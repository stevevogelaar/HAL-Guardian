# HAL Guardian — Hackathon Writeup

**GDG Windsor Build with AI — Gemma Hackathon 2026**  
**Track:** Edge / On-Device  
**Team:** HAL Guardian (Steve Vogelaar + AI collaborator)  
**License:** Apache 2.0

---

## TL;DR

HAL Guardian is a privacy-first, fully offline security assistant that runs **Google Gemma 4 through Ollama** on the user's own machine. It reviews code, scans untrusted input for prompt injection and hidden payloads, logs every action, and exposes all of this through a clean orchestrator that other agents can call. No data leaves the device unless the user chooses to export it.

---

## The Problem

AI coding assistants are convenient, but most require sending source code to a cloud API. For security-sensitive work — proprietary code, regulated environments, incident response, or simple privacy preference — that is a non-starter. Even prompt-injection testing can leak data if done remotely.

Local open models change the equation. The challenge is packaging them into a tool that is useful out of the box: structured, auditable, and easy for both humans and other agents to use.

---

## The Solution

HAL Guardian combines three security modules into one edge-deployed application:

### 1. Code Guardian
Reviews source files or pasted code for:
- **Security:** hardcoded secrets, SQL injection, unsafe execution, sensitive data exposure
- **Testing:** missing validation, silent failures, weak error handling
- **Complexity:** deep nesting, long functions, magic numbers, dead code
- **Style:** mixing concerns, unused imports, poor separation

It returns a structured verdict (`ship it` / `needs changes` / `needs discussion`) plus parsed findings with severity, category, line reference, description, and recommendation. The original Markdown review is always preserved.

### 2. Trust Shield
Scans prompts, emails, pasted text, or documents for:
- Prompt-injection command language ("ignore previous instructions", "run the following")
- Destructive imperatives (`rm -rf /`, `drop table`)
- Encoded payloads (Base64, hex, URL-encoded)
- Meta-instruction framing

A fast deterministic scan runs instantly. A **deep scan** optionally calls Gemma 4 for a second opinion on intent, severity, confidence, and recommended action.

### 3. Audit Engine
Every review and scan is appended to a local JSONL log with timestamps, targets, models, durations, success flags, and metadata. The health dashboard reports Ollama reachability and recent failure patterns.

### 4. Subagent Orchestrator
HAL Guardian is not just a UI. A central dispatcher exposes every module as a command (`review`, `review_dir`, `review_code`, `scan`, `health`, `audit`) with a standard JSON envelope. Humans can call it from the CLI, scripts can call it from PowerShell, and another AI agent can call it as a tool.

### 5. Model Playground
A free-form chat tab lets users test prompts against any local model, tune temperature, save useful prompts to the project, and browse a starter prompt library.

---

## Why Gemma 4

- **Apache 2.0 license** — free for commercial use, no API keys, no usage limits
- **Local execution** — zero latency, zero data leakage
- **Flexible quantization** — choose model size/precision for the target hardware
- **Strong reasoning** — produces structured security reviews and threat analysis without a cloud dependency

---

## Architecture

```
hal_guardian/
├── code_guardian.py       # Gemma 4 code review + Markdown parser
├── trust_shield.py        # Deterministic scanner + optional Gemma deep scan
├── audit_engine.py        # JSONL logging + health snapshots
├── orchestrator.py        # Central subagent dispatcher
├── models.py              # Shared Pydantic schemas
├── config.py              # Settings and model selection
└── prompts/               # System prompts for agents

app.py                       # Streamlit UI
orchestrate.py               # CLI entry point
tools/
└── Restart-HALGuardianUI.ps1

data/
├── sample_code/             # Demo files
├── sample_inputs/           # Demo untrusted input
└── prompts/                 # Saved + starter prompts

audits/
└── hal-guardian-audit.jsonl

docs/
├── ARCHITECTURE.md
├── ORCHESTRATOR.md
└── SCHEMA.md
```

---

## How to Run

```powershell
# Install dependencies
python -m pip install -r requirements.txt

# Make sure Ollama is running and Gemma 4 is pulled
ollama pull gemma4:e2b
ollama serve

# Launch the UI
python -m streamlit run app.py
```

---

## Demo Highlights

- **Code Guardian** reviews `data/sample_code/bad_login.php` and flags SQL injection, hardcoded credentials, and plain-text password handling as structured findings.
- **Trust Shield** scans a suspicious email, decodes a Base64 payload, and detects the destructive `rm -rf /` command.
- **Subagent Console** runs `review_dir data/sample_code` to batch-review every source file in a folder.
- **Model Playground** lets users chat with Gemma 4 and save useful prompts.
- **Audit Engine** shows every action logged locally.

---

## What's Next

- Add exportable PDF/Markdown reports from the UI
- Extend the parser to support more model output styles
- Add a `reverify` subagent that re-checks flagged findings
- Package HAL Guardian as an installable Python wheel

---

## Submission Links

- **Public repository:** (to be added after GitHub push)
- **Live demo video:** (to be recorded after final UI freeze)

HAL Guardian proves that local open models can deliver real, practical security value without sacrificing privacy.
