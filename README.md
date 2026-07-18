# HAL Guardian — Edge/On-Device AI Security Suite

**GDG Windsor Build with AI — Gemma Hackathon 2026**  
**Track:** Edge / On-Device  
**Model:** Google Gemma 4 (via Ollama)

---

## Vision

HAL Guardian is a privacy-first, fully offline security assistant that protects developers from unsafe code and untrusted inputs. It runs entirely on the user's machine using the open Gemma 4 model family — no prompts, code, or data ever leave the device.

The next generation of AI tools should not require surrendering your source code to a cloud API. HAL Guardian proves that local open models can deliver real value: code review, threat detection, and audit logging, all inside a single, easy-to-use desktop UI.

---

## What It Does

HAL Guardian combines three security modules into one swiss-army-knife tool:

### 1. Code Guardian
Reviews source files locally for:
- Security flaws (hardcoded secrets, SQL injection, unsafe execution)
- Testing gaps (missing validation, silent failures)
- Complexity issues (deep nesting, long functions, dead code)
- Style problems (naming, formatting, comments)

Returns a structured verdict: **ship it / needs changes / needs discussion**.

### 2. Trust Shield
Inspects prompts, emails, pasted text, or documents for:
- Prompt-injection command language
- Encoded payloads (Base64, hex, URL-encoded)
- Meta-instruction framing
- ADI-style metadata corruption (Agent Data Injection)

Classifies content as **trusted / untrusted / suspicious** and produces a sanitized report.

### 3. Audit Engine
Records every review and scan:
- Structured JSONL logs
- Re-verification of flagged issues
- Health dashboard with failure patterns
- Human-readable session briefs

---

## Architecture

```
hal_guardian/
├── code_guardian.py       # Gemma 4 code review engine
├── trust_shield.py        # Input sanitizer / classifier
├── audit_engine.py        # Logging, verification, health
├── models.py              # Shared Pydantic data models
├── config.py              # Settings and model selection
└── prompts/
    └── code_review.txt    # System prompt for code review

app.py                       # Streamlit UI entry point

data/
├── sample_code/           # Demo files to review
├── sample_inputs/         # Demo untrusted inputs
└── secrets/.gitkeep       # Placeholder for local-only config

audits/
└── hal-guardian-audit.jsonl  # Action log

docs/
├── ARCHITECTURE.md
├── SCHEMA.md
└── HACKATHON_WRITEUP.md
```

---

## Why Gemma 4?

- **Apache 2.0 license** — free for commercial use, no usage restrictions.
- **Local execution** — zero network latency, zero data leakage.
- **Quantization flexibility** — choose precision vs. reasoning depth for the task.
- **Tool use / structured outputs** — supports the structured reports HAL Guardian needs.

---

## Getting Started

### Prerequisites
- Python 3.12+
- Ollama installed and running
- Gemma 4 model pulled (e.g., `gemma4:e2b` or `gemma4:4b`)

### Install
```powershell
# Using HAL Python wrapper
.\tools\python-hal -m venv venv
.\venv\Scripts\Activate.ps1
.\tools\pip-hal install -r requirements.txt
```

### Run
```powershell
streamlit run app.py
```

Then open the URL shown (usually `http://localhost:8501`).

---

## Submission Deliverables

1. **Public GitHub repository** — this repo
2. **Kaggle Writeup** — `docs/HACKATHON_WRITEUP.md`
3. **Live demo** — screen recording of the Streamlit UI reviewing code and scanning untrusted input

---

## Team
Built by HAL (Steve Vogelaar's AI collaborator).

## License
Apache 2.0 — matching Gemma 4's open license.
