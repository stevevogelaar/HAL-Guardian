"""
HAL Guardian Model Comparator

Compare two local Ollama models on the same prompt, record metrics, and
optionally ask a third "judge" model to summarize the differences.
"""
import re
import time
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

import ollama

DEFAULT_OLLAMA_HOST = "http://127.0.0.1:11434"


def _similarity(a: str, b: str) -> float:
    """Simple character-level similarity score between 0.0 and 1.0."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _response_stats(text: str) -> Dict[str, Any]:
    """Basic surface metrics for a model response."""
    lines = text.splitlines()
    words = re.findall(r"\b\w+\b", text)
    return {
        "chars": len(text),
        "words": len(words),
        "lines": len(lines),
    }


def _call_model(
    model: str,
    system: str,
    prompt: str,
    temperature: float,
    num_ctx: int = 4096,
    host: str = DEFAULT_OLLAMA_HOST,
) -> Dict[str, Any]:
    """Call a single Ollama model and return a standardized result dict."""
    start = time.perf_counter()
    try:
        client = ollama.Client(host=host)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = client.chat(
            model=model,
            messages=messages,
            options={"temperature": temperature, "num_ctx": num_ctx},
        )
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        reply = response["message"]["content"]
        stats = _response_stats(reply)
        # Estimate tokens/sec using a rough chars-per-token heuristic
        est_tokens = max(1, stats["chars"] // 4)
        tokens_per_sec = round((est_tokens / (elapsed_ms / 1000.0)), 2) if elapsed_ms > 0 else 0.0
        return {
            "ok": True,
            "model": model,
            "response": reply,
            "latency_ms": elapsed_ms,
            "chars": stats["chars"],
            "words": stats["words"],
            "lines": stats["lines"],
            "estimated_tokens": est_tokens,
            "tokens_per_sec": tokens_per_sec,
        }
    except Exception as exc:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": False,
            "model": model,
            "response": "",
            "error": str(exc),
            "latency_ms": elapsed_ms,
            "chars": 0,
            "words": 0,
            "lines": 0,
            "estimated_tokens": 0,
            "tokens_per_sec": 0.0,
        }


def compare_prompt(
    active_model: str,
    compare_model: str,
    system: str,
    prompt: str,
    temperature: float,
    num_ctx: int = 4096,
    host: str = DEFAULT_OLLAMA_HOST,
) -> Dict[str, Any]:
    """
    Run the same prompt through the active model and a comparator model.
    Returns a dict with both responses and comparison metrics.
    """
    if active_model == compare_model:
        return {
            "ok": False,
            "error": "Active model and comparator model must be different.",
        }

    result_a = _call_model(active_model, system, prompt, temperature, num_ctx, host)
    result_b = _call_model(compare_model, system, prompt, temperature, num_ctx, host)

    similarity = _similarity(result_a.get("response", ""), result_b.get("response", ""))

    return {
        "ok": result_a.get("ok") and result_b.get("ok"),
        "prompt": prompt,
        "system": system,
        "temperature": temperature,
        "num_ctx": num_ctx,
        "active_model": result_a,
        "compare_model": result_b,
        "similarity": round(similarity, 3),
        "similarity_pct": f"{similarity * 100:.1f}%",
    }


def summarize_comparison(
    judge_model: str,
    prompt: str,
    response_a: Dict[str, Any],
    response_b: Dict[str, Any],
    temperature: float = 0.2,
    num_ctx: int = 4096,
    host: str = DEFAULT_OLLAMA_HOST,
) -> Dict[str, Any]:
    """
    Ask a judge model to read both responses and produce a concise comparison.
    """
    start = time.perf_counter()
    system = (
        "You are a concise technical evaluator. Compare two model responses to the same prompt. "
        "List key differences in content, tone, accuracy, and structure. Recommend which response "
        "is more useful and why. Keep your answer under 300 words."
    )
    user = (
        f"Prompt: {prompt}\n\n"
        f"--- Model A ({response_a.get('model')}) ---\n"
        f"{response_a.get('response', '')}\n\n"
        f"--- Model B ({response_b.get('model')}) ---\n"
        f"{response_b.get('response', '')}\n\n"
        "Provide your comparison."
    )
    try:
        client = ollama.Client(host=host)
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        response = client.chat(
            model=judge_model,
            messages=messages,
            options={"temperature": temperature, "num_ctx": num_ctx},
        )
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": True,
            "judge_model": judge_model,
            "summary": response["message"]["content"],
            "latency_ms": elapsed_ms,
        }
    except Exception as exc:
        return {"ok": False, "judge_model": judge_model, "error": str(exc)}
