"""
HAL Guardian Code Review Engine
Calls local Gemma 4 via Ollama to review source files.
"""
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

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


__all__ = [
    "review_file",
    "review_code",
    "suggest_fix_for_finding",
]


def _load_prompt(name: str) -> str:
    path = Path(PROMPTS_DIR) / f"{name}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    if name == "suggest_fix":
        return "You are a secure code remediation assistant. Suggest a concrete fix."
    return "You are a helpful code reviewer."


def _extract_fix(raw: str) -> str:
    """Extract the FIXED block from the model's suggested-fix response."""
    match = re.search(r"FIXED:\s*```(?:\w+)?\s*\n([\s\S]*?)\n```", raw, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: look for any fenced code block
    blocks = re.findall(r"```(?:\w+)?\s*\n([\s\S]*?)\n```", raw)
    return blocks[-1].strip() if blocks else raw.strip()


def suggest_fix_for_finding(
    code: str,
    language: str,
    finding: Finding,
    model: Optional[str] = None,
) -> str:
    """Ask Gemma 4 to suggest a concrete fix for a single finding."""
    model = model or DEFAULT_MODEL
    skill = _load_prompt("suggest_fix")
    prompt = (
        f"{skill}\n\n"
        f"LANGUAGE: {language}\n\n"
        f"FULL FILE:\n```\n{code[:MAX_FILE_CHARS]}\n```\n\n"
        f"ISSUE TO FIX:\n"
        f"Severity: {finding.severity}\n"
        f"Category: {finding.category}\n"
        f"Line(s): {finding.line}\n"
        f"Description: {finding.description}\n"
        f"Recommendation: {finding.recommendation}\n\n"
        "Provide ORIGINAL, FIXED, and EXPLANATION now."
    )
    try:
        result = _call_ollama(prompt, model)
        return _extract_fix(result["text"])
    except Exception as e:
        return f"[Could not generate fix: {e}]"


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


def _extract_summary_table(raw: str) -> dict:
    """Try to extract issue counts from the Markdown summary table.

    Falls back to inferring counts from structured headings if no table is found.
    """
    summary = {"security": 0, "testing": 0, "complexity": 0, "style": 0}

    # 1. Try explicit Markdown table: | Category | Issues Found |
    table_pattern = re.compile(
        r"\|\s*\*?\*?Category\*?\*?\s*\|\s*\*?\*?Issues?\s+Found\*?\*?\s*\|"
        r".*?\n(.*?)\n\s*\|?\s*[-=]+",
        re.IGNORECASE | re.DOTALL,
    )
    table_match = table_pattern.search(raw)
    if table_match:
        row_pattern = re.compile(r"\|\s*\*?\*?([^|*]+)\*?\*?\s*\|\s*(\d+)\s*\|")
        for match in row_pattern.finditer(table_match.group(1)):
            cat = match.group(1).strip().lower().replace("**", "").replace("*", "")
            count = int(match.group(2))
            if cat in summary:
                summary[cat] = count
        if any(v > 0 for v in summary.values()):
            return summary

    # 2. Try table without headers matching known patterns
    pattern = re.compile(r"\|\s*\*?\*?([^|*]+)\*?\*?\s*\|\s*(\d+)\s*\|", re.IGNORECASE)
    for match in pattern.finditer(raw):
        cat = match.group(1).strip().lower().replace("**", "").replace("*", "")
        count = int(match.group(2))
        if cat in summary:
            summary[cat] = count
    if any(v > 0 for v in summary.values()):
        return summary

    # 3. Fallback: infer from explicit category/severity sections
    section_map = {
        "security": r"(?:^|\n)\s*#+\s*.*(?:Security|Vulnerabilities|Security Findings).*\n",
        "testing": r"(?:^|\n)\s*#+\s*.*(?:Testing|Robustness|Error Handling).*\n",
        "complexity": r"(?:^|\n)\s*#+\s*.*(?:Complexity|Maintainability).*\n",
        "style": r"(?:^|\n)\s*#+\s*.*(?:Style|Formatting|Readability).*\n",
    }
    for cat, pat in section_map.items():
        if re.search(pat, raw, re.IGNORECASE):
            # Count severity-labeled items under that section
            section_start = re.search(pat, raw, re.IGNORECASE).end()
            section_text = raw[section_start : section_start + 3000]
            severity_counts = len(re.findall(r"\*\*Severity:\*\*\s*(critical|high|medium|low)", section_text, re.IGNORECASE))
            summary[cat] = severity_counts

    return summary


def _extract_findings(raw: str) -> List[Finding]:
    """Best-effort parser for Gemma 4 Markdown findings lists."""
    findings: List[Finding] = []

    # Split on heading patterns like #### Finding 1: ..., **1. ...**, or ### Critical Security Findings
    blocks = re.split(r"\n(?=####\s*Finding\s*\d+|\*\*\d+\.\s+.*\*\*|\*\*[A-Z][a-z]+\s+\w+.*\*\*|###\s+.*(?:Security|Testing|Complexity|Style).*)", raw, flags=re.IGNORECASE)

    severity_re = re.compile(r"\*\*Severity:\*\*\s*(critical|high|medium|low)", re.IGNORECASE)
    category_re = re.compile(r"\*\*Category:\*\*\s*(security|testing|complexity|style)", re.IGNORECASE)
    line_re = re.compile(r"\*\*Line Reference:\*\*\s*([^\n]+)", re.IGNORECASE)
    desc_re = re.compile(r"\*\*Description:\*\*\s*([\s\S]+?)(?=\*\*Recommendation:\*\*|\n\n|\Z)", re.IGNORECASE)
    rec_re = re.compile(r"\*\*Recommendation:\*\*\s*([\s\S]+?)(?=\n\n|\Z)", re.IGNORECASE)

    for block in blocks:
        if not severity_re.search(block) and not category_re.search(block):
            continue

        severity_match = severity_re.search(block)
        category_match = category_re.search(block)
        line_match = line_re.search(block)
        desc_match = desc_re.search(block)
        rec_match = rec_re.search(block)

        severity = severity_match.group(1).lower() if severity_match else "info"
        category = category_match.group(1).lower() if category_match else "general"
        line = line_match.group(1).strip() if line_match else ""

        description = ""
        if desc_match:
            description = re.sub(r"\s+", " ", desc_match.group(1)).strip()

        recommendation = ""
        if rec_match:
            recommendation = re.sub(r"\s+", " ", rec_match.group(1)).strip()
        elif not description:
            # Fallback: use the whole block as description
            description = re.sub(r"\s+", " ", block).strip()[:500]

        if description or recommendation:
            findings.append(
                Finding(
                    severity=severity,
                    category=category,
                    line=line,
                    description=description,
                    recommendation=recommendation,
                )
            )

    return findings


def _extract_verdict(raw: str) -> str:
    raw_lower = raw.lower()
    if "verdict: needs changes" in raw_lower or "verdict:** needs changes" in raw_lower:
        return "needs changes"
    if "verdict: needs discussion" in raw_lower or "verdict:** needs discussion" in raw_lower:
        return "needs discussion"
    if "verdict: ship it" in raw_lower or "verdict:** ship it" in raw_lower:
        return "ship it"
    # Fallback to first mention
    if "needs changes" in raw_lower:
        return "needs changes"
    if "needs discussion" in raw_lower:
        return "needs discussion"
    if "ship it" in raw_lower:
        return "ship it"
    return "needs discussion"


def _parse_review(raw: str) -> CodeReviewResult:
    """Parse the Gemma 4 Markdown review into a structured result."""
    verdict = _extract_verdict(raw)
    summary = _extract_summary_table(raw)
    findings = _extract_findings(raw)

    if not findings:
        # Fallback: preserve raw response as a single general finding
        findings = [
            Finding(
                severity="info",
                category="general",
                description="Model returned a free-form review. See raw response for full details.",
                recommendation="Parse and act on the review points listed by the model.",
            )
        ]

    return CodeReviewResult(
        file_path="",
        language="",
        model="",
        execution_status="completed",
        summary_table=summary,
        findings=findings,
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
