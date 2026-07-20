**Inspiration**

Solo developers and small teams are increasingly using AI coding assistants to write software faster, but they face a critical gap: no one is reviewing that AI-generated code for security vulnerabilities before it reaches production. Hiring a dedicated security team is financially impossible for a one-person operation. Worse, most AI coding tools require uploading proprietary source code to remote cloud APIs — a complete non-starter for anyone working under NDAs, in regulated industries, or handling sensitive incident response data. Even simple tasks like testing whether a prompt contains injection attacks can leak intellectual property if performed in the cloud.

We built HAL Guardian because we live this problem every day. As a solo developer managing multiple businesses — a WordPress plugin for restaurants, a security consultancy, and an AI agent infrastructure — there is no budget for a security team and no appetite for sending client code to external APIs. HAL Guardian is an edge AI security suite that runs Google Gemma 4 entirely locally on the user's own machine, reviewing code, scanning for prompt injection, validating URLs, and logging every action to a private SQLite database. Nothing ever touches a remote server unless the user explicitly opts in.

**How we built it**

We chose Gemma 4 as the sole reasoning engine because it is Apache 2.0 licensed, runs natively through Ollama on consumer hardware, and supports flexible quantization for different memory constraints. We use two variants: Gemma 4 2B for rapid preliminary scans and Gemma 4 31B for deep security analysis on complex codebases.

HAL Guardian combines five integrated modules into one desktop application. Code Guardian builds structured prompts that ask Gemma 4 to review files, pasted code, or fetched web pages for security vulnerabilities, testing gaps, complexity hotspots, and style issues. The model returns Markdown tables with Severity, Category, Line, Description, and Recommendation columns. A lightweight multi-layer parser extracts actionable findings while preserving the raw Markdown as the source of truth.

Trust Shield performs deterministic scanning plus an optional Gemma 4 deep analysis on prompts, emails, documents, and web pages to detect prompt injection language, destructive commands, and encoded payloads. It returns a trust level, confidence score, severity rating, and recommended action for each scanned input.

The Subagent Orchestrator exposes every capability as a callable command — review, review_dir, review_code, scan, health, and audit — with a standard JSON envelope. This means any other AI agent, automation script, or CI/CD pipeline can call HAL Guardian as a tool, making the entire ecosystem safer without exposing code to the cloud.

The Audit Engine records every action to both JSONL and SQLite with timestamps, targets, models used, and metadata. This creates a permanent, searchable log of every security decision the tool has ever made.

The Model Playground lets users chat directly with any pulled Ollama model, including quantized Gemma 4 variants, and save useful prompts for reuse.

All inference calls go to http://127.0.0.1:11434 via Ollama. No cloud API keys, no telemetry, no subscription fees. The stack is built with Python, Streamlit for the desktop UI, and SQLite for persistence.

**Prototype**

HAL Guardian is a functional local desktop application today, not a concept. You can run it immediately:

ollama pull gemma4:2b
python -m pip install -r requirements.txt
python -m streamlit run app.py

Or simply double-click Start-HALGuardian.bat on Windows.

We created two publicly accessible live demo pages that the tool can fetch and analyze during a screen recording:

Broken code page: https://itoversight.ca/Hal_Guardian/broken-code-page.html — contains intentional SQL injection, XSS, and hardcoded secret vulnerabilities for Guardian to detect.
Injection test page: https://itoversight.ca/Hal_Guardian/injection-test-page.html — contains prompt injection payloads and encoded commands for Trust Shield to flag.

The full source code, SQLite schema, sample data, and demo pages are available at https://github.com/stevevogelaar/HAL-Guardian.git.

**Challenges**

The most significant technical hurdle was Gemma 4's tendency to deviate from the exact Markdown output template we request, particularly for mixed-language fetched code or inputs that exceed the context window. Early versions of our parser would miss findings entirely when the model formatted its response differently than expected.

We solved this by engineering a multi-layer tolerant parser rather than fine-tuning the model. Layer one attempts to extract an explicit Markdown summary table. Layer two falls back to counting category-specific headings. Layer three always preserves the raw Markdown output as the source of truth. Layer four logs parser confidence and flags low-confidence outputs for human review. For files that exceed context limits, we added a compact-prompt fallback that truncates code and requests a shorter review, logging when the fallback is triggered. This approach turned unreliable structured outputs into reliably actionable findings without losing the model's rich qualitative analysis.

A secondary challenge was making Streamlit feel like a persistent desktop application rather than a transient script. Streamlit restarts clear UI state by default. We added a memory.py module with SQLite to persist webfetch settings, whitelist and blacklist entries, saved prompts, and the complete audit trail across restarts.

**Next steps**

Immediate priorities include adding exportable PDF and Markdown reports directly from the UI, extending the parser to support additional local model output styles beyond Gemma 4, and implementing a reverify subagent that re-checks flagged findings with a second independent prompt to reduce false positives. Longer term, we intend to package HAL Guardian as an installable Python wheel for easier distribution and explore integration with CI/CD pipelines so that every code commit can be automatically audited before merge.

HAL Guardian demonstrates that a local open model can serve as a genuine foundational asset for privacy-preserving security tooling, giving solo developers and small teams the security capabilities they need without the costs, latency, or privacy compromises of cloud-only solutions.
