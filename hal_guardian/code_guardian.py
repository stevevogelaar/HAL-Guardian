"""
HAL Guardian Code Review Engine
Calls local Gemma 4 via Ollama to review source files.
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import ollama

from .config import (
    DEFAULT_MODEL,
    MAX_FILE_CHARS,
    MAX_PROMPT_CHARS,
    COMPACT_PROMPT_CHARS,
    OLLAMA_HOST,
    OLLAMA_TIMEOUT,
    PROMPTS_DIR,
)
from .models import CodeReviewResult, Finding
from .audit_engine import log_action


def _load_prompt(name: str) -> str:
    path = Path(PROMPTS_DIR) / f"{name}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "You are a helpful code reviewer."


def _detect_language(file_path: str) -> str:
    ext = Path(file_path).suffix.lower().lstrip(".")
    lang_map = {
        "py": "python",
        "php": "php",
        "ps1": "powershell",
        "js": "javascript",
        "ts": "typescript",
        "sql": "sql",
        "html": "html",
        "css": "css",
        "md": "markdown",
        "json": "json",
        "yml": "yaml",
        "yaml": "yaml",
        "sh": "bash",
        "bat": "batch",
    }
    return lang_map.get(ext, ext)


def _truncate_code(code: str, limit: int = MAX_FILE_CHARS) -> str:
    if len(code) > limit:
        return code[:limit] + "\n\n[... truncated for review]"
    return code


def _build_prompt(skill: str, code: str, target: str, language: str, truncated: bool) -> str:
    note = "NOTE: File was truncated for review.\n\n" if truncated else ""
    return (
        f"You are HAL Guardian, a code reviewer. {skill}\n\n"
        f"TARGET FILE: {target}\n"
        f"LANGUAGE: {language}\n\n"
        f"{note}"
        f"CODE TO REVIEW:\n```\n{code}\n```\n\n"
        "Provide a structured review now."
    )


def _build_compact_prompt(code: str, target: str, language: str) -> str:
    code = code[:COMPACT_PROMPT_CHARS]
    return (
        f"Review this {language} file for security, testing, complexity, and style issues.\n"
        f"Rate: ship it / needs changes / needs discussion.\n\n"
        f"TARGET: {target}\n\nCODE:\n```\n{code}\n```\n\n"
        "Provide a concise structured review."
    )


def _call_ollama(prompt: str, model: str) -> dict:
    start = time.time()
    client = ollama.Client(host=OLLAMA_HOST)
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2, "num_ctx": 8192},
    )
    duration_ms = int((time.time() - start) * 1000)
    return {
        "text": response["message"]["content"],
        "duration_ms": duration_ms,
    }


def _parse_review(raw: str) -> CodeReviewResult:
    # Best-effort parsing: extract verdict and summary counts
    raw_lower = raw.lower()
    if "needs changes" in raw_lower:
        verdict = "needs changes"
    elif "needs discussion" in raw_lower:
        verdict = "needs discussion"
    elif "ship it" in raw_lower:
        verdict = "ship it"
    else:
        verdict = "needs discussion"

    # Count category mentions as a crude summary table
    summary = {
        "security": raw_lower.count("security"),
        "testing": raw_lower.count("testing"),
        "complexity": raw_lower.count("complexity"),
        "style": raw_lower.count("style"),
    }

    return CodeReviewResult(
        file_path="",
        language="",
        model="",
        execution_status="completed",
        summary_table=summary,
        findings=[
            Finding(
                severity="info",
                category="general",
                description="Model returned a free-form review. See raw response for full details.",
                recommendation="Parse and act on the review points listed by the model.",
            )
        ],
        verdict=verdict,
        rationale="Parsed from local Gemma 4 review output.",
        raw_response=raw,
    )


def review_file(file_path: str, model: Optional[str] = None) -> CodeReviewResult:
    target = Path(file_path)
    if not target.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    model = model or DEFAULT_MODEL
    language = _detect_language(file_path)
    code = target.read_text(encoding="utf-8", errors="ignore")
    truncated = len(code) > MAX_FILE_CHARS
    code = _truncate_code(code)

    skill = _load_prompt("code_review")
    prompt = _build_prompt(skill, code, str(target), language, truncated)

    execution_status = "ready_for_llm"
    raw_response = ""
    used_model = model

    try:
        result = _call_ollama(prompt, model)
        raw_response = result["text"]
        execution_status = "completed"
        duration_ms = result["duration_ms"]
    except Exception as e:
        # Compact retry
        execution_status = "compact_retry"
        try:
            compact = _build_compact_prompt(code, str(target), language)
            result = _call_ollama(compact, model)
            raw_response = result["text"]
            execution_status = "completed_compact"
            duration_ms = result["duration_ms"]
        except Exception as e2:
            execution_status = "model_error"
            raw_response = f"Ollama error: {e}\nCompact retry error: {e2}"
            duration_ms = 0

    review = _parse_review(raw_response)
    review.file_path = str(target)
    review.language = language
    review.model = used_model
    review.execution_status = execution_status

    success = execution_status in ("completed", "completed_compact")
    log_action(
        action_type="code_review",
        target=str(target),
        model=used_model,
        status=execution_status,
        success=success,
        output_summary=raw_response[:500],
        metadata={
            "language": language,
            "truncated": truncated,
            "prompt_chars": len(prompt),
            "duration_ms": duration_ms,
            "findings_count": len(review.findings),
        },
    )

    return review


def review_code(code: str, language: str = "text", model: Optional[str] = None) -> CodeReviewResult:
    model = model or DEFAULT_MODEL
    code = _truncate_code(code)
    skill = _load_prompt("code_review")
    prompt = _build_prompt(skill, code, "pasted-code", language, False)

    execution_status = "ready_for_llm"
    raw_response = ""
    try:
        result = _call_ollama(prompt, model)
        raw_response = result["text"]
        execution_status = "completed"
        duration_ms = result["duration_ms"]
    except Exception as e:
        execution_status = "model_error"
        raw_response = str(e)
        duration_ms = 0

    review = _parse_review(raw_response)
    review.file_path = "pasted-code"
    review.language = language
    review.model = model
    review.execution_status = execution_status

    success = execution_status == "completed"
    log_action(
        action_type="code_review",
        target="pasted-code",
        model=model,
        status=execution_status,
        success=success,
        output_summary=raw_response[:500],
        metadata={
            "language": language,
            "prompt_chars": len(prompt),
            "duration_ms": duration_ms,
            "findings_count": len(review.findings),
        },
    )

    return review
