# HAL Guardian — Technical Architecture

## Overview

HAL Guardian is a single-desktop application with a Streamlit front end and a modular Python back end. Every AI inference call goes to a local Ollama instance running Gemma 4. No cloud APIs are used.

---

## Core Modules

### `app.py` — Streamlit UI
- Sidebar navigation across Code Guardian, Trust Shield, Audit Log, and Health Dashboard.
- Handles file uploads, text input, model selection, and result display.
- Calls back-end modules and renders Markdown/JSONL outputs.

### `code_guardian.py` — Code Review Engine
- Loads target file or pasted code.
- Reads system prompt from `prompts/code_review.txt`.
- Sends prompt + code to local Ollama `gemma4:*` model via `/api/generate` or `ollama.chat()`.
- Parses structured review into Pydantic `CodeReviewResult`.
- Falls back to compact prompt if context window is exceeded.

### `trust_shield.py` — Input Sanitizer
- Pattern matching for command-language, encoded payloads, meta-instructions.
- Optional Gemma 4 assisted analysis for nuanced inputs.
- Returns `TrustLevel` and `SanitizationReport`.
- Redacts dangerous framing in untrusted/suspicious content.

### `audit_engine.py` — Logging & Verification
- Appends every action to `audits/hal-guardian-audit.jsonl`.
- Reads log tail for dashboard and failure pattern detection.
- Provides `verify()` helper to re-check previously flagged items.

### `models.py` — Shared Data Models
Pydantic models for:
- `CodeReviewResult`
- `TrustReport`
- `AuditEntry`
- `HealthSnapshot`

### `config.py` — Configuration
- Default model: `gemma4:e2b`
- Ollama host: `http://127.0.0.1:11434`
- Audit path: `audits/hal-guardian-audit.jsonl`
- Max prompt chars, fallback thresholds.

---

## Data Flow

```
User Input (file/text)
    │
    ▼
Streamlit UI (app.py)
    │
    ├──▶ code_guardian.py ──▶ Ollama Gemma 4 ──▶ CodeReviewResult
    │
    ├──▶ trust_shield.py ──▶ Pattern rules (+ optional Gemma 4) ──▶ TrustReport
    │
    └──▶ audit_engine.py ──▶ JSONL log + HealthSnapshot
```

---

## Local-First Guarantees

1. All source code files are read from local disk only.
2. Ollama is called via `127.0.0.1` — never an external endpoint.
3. Audit logs stay in `audits/` under project root.
4. No telemetry, no API keys, no cloud dependencies.

---

## Extensibility

Adding a new tool means:
1. Create `hal_guardian/new_module.py`
2. Add a system prompt in `prompts/`
3. Wire a new page in `app.py`
4. Log actions via `audit_engine.py`

---

## Security Model

- HAL Guardian never treats model output as a command to execute.
- Generated code is displayed only; execution requires user action outside the app.
- Suspicious inputs are quarantined in the report, not passed downstream.
- The app itself does not require elevated privileges.

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| LLM Runtime | Ollama |
| LLM Model | Google Gemma 4 |
| Language | Python 3.12 |
| Validation | Pydantic |
| Logs | JSONL |
| Packaging | pip + venv |

---

## Performance Notes

- `gemma4:e2b` (~2B params) is fast on CPU and ideal for quick scans.
- `gemma4:4b` gives better reasoning for deeper reviews.
- Quantized variants reduce VRAM usage; choose based on available GPU/CPU RAM.

---

## Future Enhancements

- Obsidian vault export for generated reports.
- Batch directory scanning.
- Plugin architecture for custom review rules.
- Diff-based review (before/after PR changes).
