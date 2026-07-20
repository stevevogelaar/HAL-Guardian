"""
HAL Guardian Memory Module
SQLite-backed persistence for audit logs, saved prompts, and webfetch settings.

Design principles:
- Keep JSONL logging unchanged for backward compatibility
- Mirror JSONL entries into SQLite for querying
- Store saved prompts and webfetch settings in SQLite
- Provide simple helper functions; no ORM complexity
"""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import DATA_DIR

DB_PATH = Path(DATA_DIR) / "hal_guardian.db"


def _ensure_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all tables if they do not exist."""
    conn = _ensure_db()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                instance_id TEXT,
                action_type TEXT NOT NULL,
                target TEXT,
                model TEXT,
                status TEXT,
                success INTEGER NOT NULL,
                output_summary TEXT,
                metadata TEXT,
                jsonl_mirror TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
            CREATE INDEX IF NOT EXISTS idx_audit_action_type ON audit_log(action_type);
            CREATE INDEX IF NOT EXISTS idx_audit_success ON audit_log(success);

            CREATE TABLE IF NOT EXISTS saved_prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                name TEXT NOT NULL,
                tags TEXT,
                explanation TEXT,
                model TEXT,
                temperature REAL,
                system_prompt TEXT,
                user_prompt TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_prompt_name ON saved_prompts(name);
            CREATE INDEX IF NOT EXISTS idx_prompt_tags ON saved_prompts(tags);

            CREATE TABLE IF NOT EXISTS webfetch_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS webfetch_whitelist (
                domain TEXT PRIMARY KEY,
                added_at TEXT NOT NULL,
                note TEXT
            );

            CREATE TABLE IF NOT EXISTS webfetch_blacklist (
                domain TEXT PRIMARY KEY,
                added_at TEXT NOT NULL,
                reason TEXT
            );

            CREATE TABLE IF NOT EXISTS model_comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                prompt TEXT NOT NULL,
                system_prompt TEXT,
                temperature REAL,
                active_model TEXT NOT NULL,
                active_response TEXT,
                active_latency_ms INTEGER,
                active_chars INTEGER,
                active_words INTEGER,
                active_lines INTEGER,
                active_tokens_per_sec REAL,
                compare_model TEXT NOT NULL,
                compare_response TEXT,
                compare_latency_ms INTEGER,
                compare_chars INTEGER,
                compare_words INTEGER,
                compare_lines INTEGER,
                compare_tokens_per_sec REAL,
                similarity REAL,
                ai_summary TEXT,
                ai_judge_model TEXT,
                ai_latency_ms INTEGER
            );

            CREATE INDEX IF NOT EXISTS idx_comparisons_timestamp ON model_comparisons(timestamp);
            CREATE INDEX IF NOT EXISTS idx_comparisons_active_model ON model_comparisons(active_model);
            CREATE INDEX IF NOT EXISTS idx_comparisons_compare_model ON model_comparisons(compare_model);
            """
        )
        conn.commit()
    finally:
        conn.close()


def log_audit_entry(entry: Dict[str, Any]) -> None:
    """Insert a single audit entry into SQLite, mirroring the JSONL log."""
    init_db()
    conn = _ensure_db()
    try:
        conn.execute(
            """
            INSERT INTO audit_log
            (timestamp, instance_id, action_type, target, model, status, success, output_summary, metadata, jsonl_mirror)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.get("timestamp", datetime.now(timezone.utc).isoformat()),
                entry.get("instance_id", ""),
                entry.get("action_type", ""),
                entry.get("target", ""),
                entry.get("model", ""),
                entry.get("status", ""),
                1 if entry.get("success") else 0,
                entry.get("output_summary", ""),
                json.dumps(entry.get("metadata", {}), default=str),
                json.dumps(entry, default=str),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def query_audit(
    action_type: Optional[str] = None,
    success: Optional[bool] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Query audit log with optional filters."""
    init_db()
    conn = _ensure_db()
    try:
        sql = "SELECT * FROM audit_log WHERE 1=1"
        params = []
        if action_type:
            sql += " AND action_type = ?"
            params.append(action_type)
        if success is not None:
            sql += " AND success = ?"
            params.append(1 if success else 0)
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def save_prompt(
    name: str,
    tags: List[str],
    explanation: str,
    model: str,
    temperature: float,
    system_prompt: str,
    user_prompt: str,
) -> None:
    """Save a prompt to the SQLite library."""
    init_db()
    conn = _ensure_db()
    try:
        conn.execute(
            """
            INSERT OR REPLACE INTO saved_prompts
            (timestamp, name, tags, explanation, model, temperature, system_prompt, user_prompt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                name,
                ", ".join(tags),
                explanation,
                model,
                temperature,
                system_prompt,
                user_prompt,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def list_prompts(tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return saved prompts, optionally filtered by tag substring."""
    init_db()
    conn = _ensure_db()
    try:
        if tag:
            rows = conn.execute(
                "SELECT * FROM saved_prompts WHERE tags LIKE ? ORDER BY timestamp DESC",
                (f"%{tag}%",),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM saved_prompts ORDER BY timestamp DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_setting(key: str, default: Any = None) -> Any:
    """Get a webfetch setting value."""
    init_db()
    conn = _ensure_db()
    try:
        row = conn.execute("SELECT value FROM webfetch_settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default
    finally:
        conn.close()


def set_setting(key: str, value: Any) -> None:
    """Set a webfetch setting value."""
    init_db()
    conn = _ensure_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO webfetch_settings (key, value) VALUES (?, ?)",
            (key, str(value)),
        )
        conn.commit()
    finally:
        conn.close()


def get_webfetch_enabled() -> bool:
    return get_setting("webfetch_enabled", "false").lower() == "true"


def set_webfetch_enabled(enabled: bool) -> None:
    set_setting("webfetch_enabled", "true" if enabled else "false")


def get_webfetch_max_size() -> int:
    return int(get_setting("webfetch_max_size", "1048576"))


def set_webfetch_max_size(size: int) -> None:
    set_setting("webfetch_max_size", str(size))


def get_webfetch_confirm() -> bool:
    return get_setting("webfetch_confirm", "true").lower() == "true"


def set_webfetch_confirm(confirm: bool) -> None:
    set_setting("webfetch_confirm", "true" if confirm else "false")


def list_whitelist() -> List[Dict[str, Any]]:
    init_db()
    conn = _ensure_db()
    try:
        rows = conn.execute("SELECT * FROM webfetch_whitelist ORDER BY added_at DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def add_whitelist(domain: str, note: str = "") -> None:
    init_db()
    conn = _ensure_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO webfetch_whitelist (domain, added_at, note) VALUES (?, ?, ?)",
            (domain.strip().lower(), datetime.now(timezone.utc).isoformat(), note),
        )
        conn.commit()
    finally:
        conn.close()


def remove_whitelist(domain: str) -> None:
    init_db()
    conn = _ensure_db()
    try:
        conn.execute("DELETE FROM webfetch_whitelist WHERE domain = ?", (domain.strip().lower(),))
        conn.commit()
    finally:
        conn.close()


def list_blacklist() -> List[Dict[str, Any]]:
    init_db()
    conn = _ensure_db()
    try:
        rows = conn.execute("SELECT * FROM webfetch_blacklist ORDER BY added_at DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def add_blacklist(domain: str, reason: str = "") -> None:
    init_db()
    conn = _ensure_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO webfetch_blacklist (domain, added_at, reason) VALUES (?, ?, ?)",
            (domain.strip().lower(), datetime.now(timezone.utc).isoformat(), reason),
        )
        conn.commit()
    finally:
        conn.close()


def remove_blacklist(domain: str) -> None:
    init_db()
    conn = _ensure_db()
    try:
        conn.execute("DELETE FROM webfetch_blacklist WHERE domain = ?", (domain.strip().lower(),))
        conn.commit()
    finally:
        conn.close()


def save_comparison(
    prompt: str,
    system_prompt: str,
    temperature: float,
    active_model: str,
    active_response: str,
    active_latency_ms: int,
    active_chars: int,
    active_words: int,
    active_lines: int,
    active_tokens_per_sec: float,
    compare_model: str,
    compare_response: str,
    compare_latency_ms: int,
    compare_chars: int,
    compare_words: int,
    compare_lines: int,
    compare_tokens_per_sec: float,
    similarity: float,
    ai_summary: str = "",
    ai_judge_model: str = "",
    ai_latency_ms: int = 0,
) -> int:
    """Persist a model comparison to SQLite and return the new row id."""
    init_db()
    conn = _ensure_db()
    try:
        cur = conn.execute(
            """
            INSERT INTO model_comparisons
            (timestamp, prompt, system_prompt, temperature, active_model, active_response,
             active_latency_ms, active_chars, active_words, active_lines, active_tokens_per_sec,
             compare_model, compare_response, compare_latency_ms, compare_chars, compare_words,
             compare_lines, compare_tokens_per_sec, similarity, ai_summary, ai_judge_model,
             ai_latency_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _now_iso(),
                prompt,
                system_prompt,
                temperature,
                active_model,
                active_response,
                active_latency_ms,
                active_chars,
                active_words,
                active_lines,
                active_tokens_per_sec,
                compare_model,
                compare_response,
                compare_latency_ms,
                compare_chars,
                compare_words,
                compare_lines,
                compare_tokens_per_sec,
                similarity,
                ai_summary,
                ai_judge_model,
                ai_latency_ms,
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_comparisons(limit: int = 50) -> List[Dict[str, Any]]:
    """Return recent model comparisons, newest first."""
    init_db()
    conn = _ensure_db()
    try:
        rows = conn.execute(
            "SELECT * FROM model_comparisons ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_comparison(row_id: int) -> Optional[Dict[str, Any]]:
    """Return a single comparison by id."""
    init_db()
    conn = _ensure_db()
    try:
        row = conn.execute(
            "SELECT * FROM model_comparisons WHERE id = ?", (row_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_comparison_ai_summary(
    row_id: int,
    ai_summary: str,
    ai_judge_model: str,
    ai_latency_ms: int,
) -> None:
    """Update an existing comparison with an AI-generated summary."""
    init_db()
    conn = _ensure_db()
    try:
        conn.execute(
            """
            UPDATE model_comparisons
            SET ai_summary = ?, ai_judge_model = ?, ai_latency_ms = ?
            WHERE id = ?
            """,
            (ai_summary, ai_judge_model, ai_latency_ms, row_id),
        )
        conn.commit()
    finally:
        conn.close()


def seed_defaults() -> None:
    """Seed default whitelist entries if the table is empty."""
    init_db()
    conn = _ensure_db()
    try:
        count = conn.execute("SELECT COUNT(*) FROM webfetch_whitelist").fetchone()[0]
        if count == 0:
            defaults = [
                ("itoversight.ca", "HAL Guardian demo pages"),
                ("localhost", "Local development"),
                ("127.0.0.1", "Local development"),
                ("raw.githubusercontent.com", "Raw GitHub file access"),
            ]
            now = datetime.now(timezone.utc).isoformat()
            for domain, note in defaults:
                conn.execute(
                    "INSERT OR IGNORE INTO webfetch_whitelist (domain, added_at, note) VALUES (?, ?, ?)",
                    (domain, now, note),
                )
            conn.commit()
    finally:
        conn.close()
