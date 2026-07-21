# HAL Guardian — Edge/On-Device AI Security Suite

**GDG Windsor Build with AI — Gemma Hackathon 2026**  
**Track:** Edge / On-Device  
**Model:** Google Gemma 4 (via Ollama)  
**License:** Apache 2.0  
**Team:** Steve Vogelaar & HAL (AI collaborator)  
HAL is an accredited co-contributor: architecture, code, documentation, and QA.

---

## Vision

HAL Guardian is a privacy-first, fully offline security assistant that protects developers from unsafe code and untrusted inputs. It runs entirely on the user's machine using the open Gemma 4 model family — no prompts, code, or data ever leave the device unless the user explicitly enables the optional webfetch feature.

The next generation of AI tools should not require surrendering your source code to a cloud API. HAL Guardian proves that local open models can deliver real value: code review, threat detection, audit logging, and prompt experimentation, all inside a single, easy-to-use desktop UI.

---

## What It Does

HAL Guardian combines five layers into one edge-deployed security assistant:

### 1. Code Guardian
Reviews source files, pasted code, or fetched web pages locally for:
- **Security** — hardcoded secrets, SQL injection, unsafe execution, sensitive data exposure
- **Testing** — missing validation, silent failures, weak error handling
- **Complexity** — deep nesting, long functions, magic numbers, dead code
- **Style** — naming, formatting, mixing concerns, unused imports

Returns a structured verdict (`ship it` / `needs changes` / `needs discussion`) plus parsed findings with severity, category, line reference, description, and recommendation. The full model response is always preserved as `Raw review (Markdown)`. For `critical`, `high`, or `medium` findings, click **Suggest fix** to request a safe code replacement.

### 2. Trust Shield
Scans prompts, emails, pasted text, documents, or fetched web pages for:
- Prompt-injection command language
- Destructive imperatives (`rm -rf /`, `drop table`, etc.)
- Encoded payloads (Base64, hex, URL-encoded)
- Meta-instruction framing

Quick scan is deterministic and instant. **Deep scan** calls Gemma 4 for a second opinion on intent, severity, confidence, and recommended action. A redacted / sanitized copy of the input is shown at the bottom for safe sharing.

### 3. Audit Engine
Records every review and scan:
- Structured JSONL logs in `audits/hal-guardian-audit.jsonl`
- SQLite-backed persistence for audit entries, saved prompts, and webfetch settings
- Health dashboard with Ollama reachability and failure-pattern detection

### 4. Subagent Orchestrator
Every module is exposed as a command (`review`, `review_dir`, `review_code`, `scan`, `health`, `audit`) with a standard JSON envelope. Use it from the UI, CLI, Python, PowerShell, or another AI agent.

### 5. Model Playground
A free-form local-LLM chat for prompt testing. Load examples, generate random prompts, tune temperature, chat with any Ollama model, and save useful prompts to the project library.

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
├── memory.py              # SQLite persistence for settings + saved prompts + audit logs
├── webfetch.py            # Safe, user-controlled URL fetcher
├── document_extract.py    # Text extraction for txt/md/eml/pdf/docx/images
└── prompts/
    ├── code_review.txt    # System prompt for code review
    ├── trust_deep.txt     # System prompt for deep trust analysis
    └── starter.json       # Starter prompts for the Model Playground

app.py                       # Streamlit UI entry point
orchestrate.py               # CLI entry point for subagents
Start-HALGuardian.bat        # One-click launcher

audits/
└── hal-guardian-audit.jsonl

data/
├── sample_code/             # Demo files to review
├── sample_inputs/           # Demo untrusted input
├── live-docs/               # Live demo HTML pages for webfetch testing
└── prompts/                 # Starter + saved prompts

frontend/
├── start.ps1
└── Stop-HALGuardianUI.ps1

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

See [`QUICKSTART.md`](QUICKSTART.md) for the fastest path from install to running UI.

### Prerequisites
- Python 3.12+
- Ollama installed and running
- Gemma 4 model pulled (e.g., `gemma4:e2b` or `gemma4:4b`)

### Install
```powershell
# Pull the default local model
ollama pull gemma4:e2b

# Install Python dependencies
python -m pip install -r requirements.txt
```

### Run

**Easiest:** double-click `Start-HALGuardian.bat` in this folder.  
A terminal opens, starts Streamlit, and prints `http://localhost:8501`.  
Leave the terminal open and open that URL in your browser.

Or from PowerShell:
```powershell
python -m streamlit run app.py
```

Then open the URL shown (usually `http://localhost:8501`).

> **Note:** switching sidebar modules while a local model is running will cancel the current operation. Wait for results before changing tabs.

---

## Webfetch (Optional, Disabled by Default)

Code Guardian and Trust Shield can fetch a live URL for analysis. Because this feature carries real security and privacy risks, it is **off by default** and protected by a domain whitelist.

HAL Guardian is a local proof-of-concept, not enterprise-grade isolation software. Live webfetch can:
- Send fetched content to your local Ollama model, including any malicious payloads on the page.
- Reveal your IP address and environment details to the remote site.
- Allow requests to internal services or cloud metadata endpoints if the whitelist is misconfigured.
- Expose information about what is reachable from your machine through network errors or redirects.

Recommended controls:
1. Keep webfetch disabled unless you need it for a specific demo.
2. Only whitelist domains you control or fully trust.
3. Enable **Require confirmation before sending fetched content to LLM**.
4. Keep **Max download size** small.
5. Never point it at internal admin panels or cloud metadata URLs.

Live demo pages for testing webfetch:
- `https://itoversight.ca/Hal_Guardian/broken-code-page.html`
- `https://itoversight.ca/Hal_Guardian/injection-test-page.html`

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

1. **Public GitHub repository** — https://github.com/stevevogelaar/HAL-Guardian.git
2. **Kaggle Writeup** — [`docs/HACKATHON_WRITEUP.md`](docs/HACKATHON_WRITEUP.md)
3. **Live demo video** — screen recording of the Streamlit UI reviewing code, scanning untrusted input, batch-reviewing a directory, and using the Model Playground

---

## Team
Co-created by **Steve Vogelaar** and **HAL** (AI collaborator).  
HAL is an accredited co-contributor on this submission and holds joint domain over all work produced in this collaboration, per the Salamander Collaboration Agreement.

## License
Apache 2.0 — matching Gemma 4's open license.
