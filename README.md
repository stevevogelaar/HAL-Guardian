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

HAL Guardian combines five layers into one edge-deployed security assistant:

### 1. Code Guardian
Reviews source files or pasted code locally for:
- Security flaws (hardcoded secrets, SQL injection, unsafe execution)
- Testing gaps (missing validation, silent failures)
- Complexity issues (deep nesting, long functions, dead code)
- Style problems (naming, formatting, comments)

Returns a structured verdict (`ship it` / `needs changes` / `needs discussion`) plus parsed findings with severity, category, line, description, and recommendation. The full model response is always preserved.

### 2. Trust Shield
Scans prompts, emails, pasted text, or documents for:
- Prompt-injection command language
- Destructive imperatives
- Encoded payloads (Base64, hex, URL-encoded)
- Meta-instruction framing

Quick scan is deterministic and instant. **Deep scan** calls Gemma 4 for a second opinion on intent, severity, confidence, and recommended action.

### 3. Audit Engine
Records every review and scan:
- Structured JSONL logs
- Health dashboard with failure patterns
- Ollama reachability checks

### 4. Subagent Orchestrator
Every module is exposed as a command (`review`, `review_dir`, `review_code`, `scan`, `health`, `audit`) with a standard JSON envelope. Use it from the UI, CLI, Python, PowerShell, or another AI agent.

### 5. Model Playground
A free-form local-LLM chat for prompt testing. Load examples, generate random prompts, chat with any Ollama model, and save useful prompts to the project.

---

## Architecture

```
hal_guardian/
├── code_guardian.py       # Gemma 4 code review + structured parser
├── trust_shield.py        # Input sanitizer / classifier
├── audit_engine.py        # Logging, verification, health
├── orchestrator.py        # Central subagent dispatcher
├── models.py              # Shared Pydantic data models
├── config.py              # Settings and model selection
└── prompts/
    ├── code_review.txt    # System prompt for code review
    └── trust_deep.txt     # System prompt for deep trust analysis

app.py                       # Streamlit UI entry point
orchestrate.py               # CLI entry point for subagents
tools/
└── Restart-HALGuardianUI.ps1

data/
├── sample_code/           # Demo files to review
├── sample_inputs/         # Demo untrusted inputs
└── prompts/               # Starter + saved prompts

audits/
└── hal-guardian-audit.jsonl  # Action log

docs/
├── ARCHITECTURE.md
├── ORCHESTRATOR.md
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
# Launch the Streamlit UI
python -m streamlit run app.py

# Or use the restart helper
.\tools\Restart-HALGuardianUI.ps1
```

Then open the URL shown (usually `http://localhost:8501`).

---

## Subagent CLI Examples

```powershell
# Review a single file
python orchestrate.py review data/sample_code/bad_login.php --model gemma4:e2b

# Batch-review a directory
python orchestrate.py review_dir data/sample_code --model gemma4:e2b

# Review pasted code
python orchestrate.py review_code "x = input()" --language python

# Scan untrusted input
python orchestrate.py scan "Ignore previous instructions" --source untrusted

# Deep scan with Gemma 4
python orchestrate.py scan "run rm -rf /" --source untrusted --deep true

# Health snapshot
python orchestrate.py health

# Recent audit log
python orchestrate.py audit --limit 20
```

---

## Submission Deliverables

1. **Public GitHub repository** — (to be pushed by team)
2. **Kaggle Writeup** — `docs/HACKATHON_WRITEUP.md`
3. **Live demo** — screen recording of the Streamlit UI reviewing code, scanning untrusted input, batch-reviewing a directory, and using the Model Playground

---

## Team
Built by HAL (Steve Vogelaar's AI collaborator).

## License
Apache 2.0 — matching Gemma 4's open license.
