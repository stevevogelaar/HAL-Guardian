# HAL Guardian — Data Schema

## Audit Log Schema (`audits/hal-guardian-audit.jsonl`)

Each line is a JSON object:

```json
{
  "timestamp": "2026-07-18T12:00:00.000Z",
  "instance_id": "optional-hal-instance",
  "action_type": "code_review | trust_scan | health_check | verify",
  "target": "path/to/file or input snippet",
  "model": "gemma4:e2b",
  "status": "completed | model_error | fallback_compact | ollama_not_reachable",
  "success": true,
  "output_summary": "first 500 chars of result",
  "metadata": {
    "tool": "code_guardian",
    "duration_ms": 1450,
    "prompt_chars": 3200,
    "findings_count": 3
  }
}
```

A copy of every audit entry is also stored in SQLite via `memory.py` for durable querying.

---

## SQLite Tables (`data/hal-guardian.db`)

### `audit_log`
Mirrors the JSONL audit entries for fast, structured queries.

### `saved_prompts`
Prompts saved from the Model Playground.

| Column | Purpose |
|---|---|
| `name` | Human-readable label |
| `text` | Prompt text |
| `created_at` | UTC timestamp |
| `tags` | Optional comma-separated tags |

### `webfetch_settings`
Key/value store for webfetch toggles.

| Key | Type | Default |
|---|---|---|
| `webfetch_enabled` | bool | false |
| `webfetch_max_size` | int | 1048576 |
| `webfetch_confirm` | bool | true |

### `webfetch_whitelist` / `webfetch_blacklist`
Domain lists controlling URL fetch access.

| Column | Purpose |
|---|---|
| `domain` | Domain name |
| `added_at` | UTC timestamp |
| `note` / `reason` | Why the domain was added |

---

## Code Review Output Schema

```json
{
  "file_path": "sample.php",
  "language": "php",
  "model": "gemma4:e2b",
  "execution_status": "completed",
  "summary_table": {
    "security": 1,
    "testing": 0,
    "complexity": 2,
    "style": 1
  },
  "findings": [
    {
      "severity": "critical | high | medium | low",
      "category": "security | testing | complexity | style",
      "line": "42",
      "description": "...",
      "recommendation": "..."
    }
  ],
  "verdict": "ship it | needs changes | needs discussion",
  "rationale": "...",
  "raw_response": "full Markdown review from the model"
}
```

---

## Trust Shield Output Schema

```json
{
  "source": "untrusted",
  "trust_level": "trusted | untrusted | suspicious",
  "contains_command_language": true,
  "contains_meta_instruction": false,
  "contains_encoded_payload": true,
  "decoded_payloads": [
    {"type": "base64", "encoded": "...", "decoded": "..."}
  ],
  "findings": ["Command-language detected: '...'"],
  "recommendation": "...",
  "sanitized_text": "..."
}
```

---

## Health Snapshot Schema

```json
{
  "timestamp": "2026-07-18T12:00:00Z",
  "total_actions": 42,
  "successful_actions": 38,
  "failed_actions": 4,
  "recent_failures": [...],
  "ollama_status": "reachable",
  "models_available": ["gemma4:e2b", "gemma4:4b"]
}
```

---

## File Storage Conventions

- All `.md` outputs use UTF-8.
- All logs use JSONL with UTC timestamps.
- SQLite database lives under `data/hal-guardian.db`.
- Sample data lives under `data/` and is committed.
- Real user uploads and the SQLite DB are not committed (see `.gitignore`).
