# HAL Guardian — Edge/On-Device AI Security Suite

**GDG Windsor Build with AI — Gemma Hackathon 2026**  
**Track:** Edge / On-Device  
**Team:** Steve Vogelaar \& HAL (AI collaborator)  
HAL is an accredited co-contributor responsible for architecture, code review, documentation, and quality assurance.
**License:** Apache 2.0

---

## Summary

HAL Guardian is a privacy-first security assistant that runs **Google Gemma 4 through Ollama** entirely on the user's own machine. It reviews code, scans untrusted input for prompt injection and hidden payloads, logs every action to a local SQLite-backed store, and exposes every module as an agent-callable command. The project proves that a local open model can deliver real, practical security value without sending proprietary code or prompts to a cloud API. It is a proof-of-concept desktop tool, not enterprise-grade isolation software.

---

## Problem

Most AI coding assistants require uploading source code to a remote API. That is unacceptable for proprietary code, regulated environments, incident response, or anyone who simply values privacy. Even prompt-injection testing can leak data if done remotely. The challenge is packaging a local open model into a tool that is structured, auditable, and useful out of the box.

---

## Solution

HAL Guardian combines five layers into one desktop application:

1. **Code Guardian** reviews files, pasted code, or fetched web pages for security, testing, complexity, and style issues, returning a verdict and structured findings.
2. **Trust Shield** scans prompts, emails, documents, and web pages for prompt-injection language, destructive commands, and encoded payloads, with an optional Gemma 4 deep scan.
3. **Audit Engine** records every action to JSONL and SQLite with timestamps, targets, models, and metadata.
4. **Subagent Orchestrator** exposes every module as a command (`review`, `review_dir`, `review_code`, `scan`, `health`, `audit`, `compare`) with a standard JSON envelope, so scripts or other agents can call HAL Guardian as a tool.
5. **Model Playground** lets users chat with any local Ollama model and save useful prompts. Enable the comparator to run the same prompt through two models, view side-by-side metrics (latency, length, similarity), and ask a judge model to summarize the differences.

### Why Edge / On-Device?

Running locally matters for three reasons. **Privacy:** proprietary source code and sensitive prompts never leave the machine. **Cost and latency:** no per-token cloud bills and no network round-trips. **Compliance and control:** regulated environments and incident responders can review code without vendor lock-in or external data-processing agreements. Gemma 4's Apache 2.0 license and flexible Ollama quantization make this practical on consumer hardware.

Document and image extraction, URL fetching, model inference, and logging all happen locally by default. Optional webfetch is opt-in, whitelist-controlled, and confirm-before-send.

---

## Architecture

The stack is modular and local-first:

- `app.py` — Streamlit UI with sidebar navigation and module pages.
- `hal_guardian/code_guardian.py` — builds prompts, calls Ollama, parses Markdown reviews.
- `hal_guardian/trust_shield.py` — deterministic scanner plus optional Gemma 4 deep analysis.
- `hal_guardian/orchestrator.py` — central dispatcher for all subagent commands.
- `hal_guardian/audit_engine.py` + `memory.py` — JSONL and SQLite persistence.
- `hal_guardian/webfetch.py` — safe URL fetcher with whitelist and confirmation.
- `hal_guardian/document_extract.py` — local extraction from txt/md/eml/pdf/docx/images.
- `prompts/` — system prompts and saved prompt library.
- `audits/` and `data/` — local logs, SQLite DB, sample data, and live demo HTML pages.

All inference calls go to `http://127.0.0.1:11434`. No cloud APIs, telemetry, or API keys are required.

---

## How Gemma 4 Is Used

Gemma 4 is the reasoning engine behind every AI-driven feature:

- **Code Guardian** sends a structured prompt with the target file, language, and a request for categorized findings. The model returns Markdown with severity, category, line reference, description, and recommendation. A lightweight parser extracts structured findings while the full Markdown is preserved.
- **Trust Shield Deep Scan** sends suspicious text to Gemma 4 for intent analysis, returning trust level, confidence, severity, and recommended action.
- **Model Playground** lets users chat directly with any pulled Ollama model, including quantized variants.
- **Suggest Fix** asks Gemma 4 to produce a safe code replacement for a specific finding.

We use Gemma 4 because it is Apache 2.0 licensed, runs locally through Ollama, supports flexible quantization, and produces structured security analysis without a cloud dependency. For hackathon demos we default to `gemma4:e2b` (2B) for speed, while users can choose larger quantizations for deeper analysis.

---

## Challenges and Decisions

### Mixed model output formats
Gemma 4 does not always use the exact Markdown template we request, especially for mixed-language fetched code or long inputs. We solved this by making the parser tolerant: it looks for an explicit summary table, falls back to counting category-specific headings, and always keeps the raw Markdown as the source of truth.

### Long inputs exceeding context
Large files can exceed the 8K context window. We added a compact-prompt fallback that truncates code and asks for a shorter review, then logs when the fallback is used.

### Document and image extraction
Users want to drop in PDFs, emails, or screenshots. We added `document_extract.py` to handle `txt/md/eml/pdf/docx` and read metadata plus text comments from images locally, keeping the privacy promise intact.

### Safe live webfetch
Fetching URLs introduces SSRF, privacy, and payload risks. We made webfetch disabled by default, restricted by a domain whitelist, gated by a confirmation checkbox, and size-limited. This lets the demo analyze live pages without exposing the user by default.

### Persistent settings across restarts
Streamlit restarts clear UI state. We added `memory.py` with SQLite to persist webfetch settings, whitelist/blacklist, saved prompts, and audit logs, so the tool feels like a real desktop app rather than a transient script.

---

## Live Demo

HAL Guardian is a local desktop application, so the live demo is provided as publicly accessible test pages that the UI can fetch and analyze during a screen recording:

- **Broken code page:** `https://itoversight.ca/Hal_Guardian/broken-code-page.html`
- **Injection test page:** `https://itoversight.ca/Hal_Guardian/injection-test-page.html`

To run the application locally:

```powershell
ollama pull gemma4:e2b
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Or double-click `Start-HALGuardian.bat`.

---

## Project Links

- **Public code repository:** https://github.com/stevevogelaar/HAL-Guardian.git
- **Live demo pages:** https://itoversight.ca/Hal_Guardian/
- **Video walkthrough:** (to be recorded after final UI freeze)

---

## Next Steps

- Exportable PDF/Markdown reports from the UI
- Extend the parser for more model output styles
- Add a `reverify` subagent that re-checks flagged findings
- Package HAL Guardian as an installable Python wheel
- Integrate Google Cloud's Guardian API for online content moderation in addition to the local pipeline (hackathon bonus)

HAL Guardian demonstrates that local open models can serve as a strong foundational asset for privacy-preserving security tooling.
