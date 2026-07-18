"""
HAL Guardian Audit Engine
Logs every action to JSONL and provides health/verification helpers.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .config import AUDIT_PATH
from .models import AuditEntry
from .memory import log_audit_entry as _log_to_sql, init_db as _init_memory_db


def _ensure_audit_dir():
    Path(AUDIT_PATH).parent.mkdir(parents=True, exist_ok=True)


def log_action(
    action_type: str,
    target: str,
    model: str = "",
    status: str = "",
    success: bool = False,
    output_summary: str = "",
    metadata: Optional[dict] = None,
) -> AuditEntry:
    _ensure_audit_dir()
    _init_memory_db()
    entry = AuditEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        action_type=action_type,
        target=target[:500],
        model=model,
        status=status,
        success=success,
        output_summary=output_summary[:500],
        metadata=metadata or {},
    )
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(entry.model_dump_json() + "\n")
    _log_to_sql(entry.model_dump())
    return entry


def read_audit_tail(limit: int = 50) -> List[dict]:
    if not Path(AUDIT_PATH).exists():
        return []
    with open(AUDIT_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    records = []
    for line in lines[-limit:]:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def health_snapshot() -> dict:
    records = read_audit_tail(limit=1000)
    total = len(records)
    successes = sum(1 for r in records if r.get("success"))
    failures = [r for r in records if not r.get("success")][-5:]

    # Check Ollama reachability
    ollama_status = "unknown"
    models_available = []
    try:
        import requests
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if r.ok:
            ollama_status = "reachable"
            models_available = [m.get("name") for m in r.json().get("models", [])]
        else:
            ollama_status = "error"
    except Exception:
        ollama_status = "not_reachable"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_actions": total,
        "successful_actions": successes,
        "failed_actions": total - successes,
        "recent_failures": failures,
        "ollama_status": ollama_status,
        "models_available": models_available,
    }
