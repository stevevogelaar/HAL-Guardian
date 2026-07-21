# HAL Guardian — Educational Demo Video Script

**Project type:** Local proof-of-concept AI security assistant  
**Tone:** Educational, technical demo — not promotional  
**Target final length:** 4:00 – 5:30  
**Voice:** Clear, direct, instructional; second-person is acceptable but avoid sales language  
**Recording:** Screen capture of local Streamlit UI + separate voice-over in DaVinci Resolve  
**Editing:** Jump cuts over model-thinking time are expected and helpful

---

## Section 1 — Introduction (0:00–0:45)

**Shot:** Title card, then fade into the HAL Guardian Home page.

**Script:**
> HAL Guardian is a proof-of-concept, local-first security assistant. It uses Google's Gemma 4 model, served through Ollama, to analyze code and untrusted input without sending data to a cloud API.
>
> This demo walks through the tool's architecture, its security model, and each of its modules: Code Guardian, Trust Shield, Audit Engine, Subagent Console, and Model Playground.
>
> Everything shown runs on this machine. The model endpoint is `127.0.0.1:11434`. There are no API keys, no telemetry, and no remote inference by default. Audit entries, saved prompts, webfetch settings, and the whitelist are persisted locally with SQLite and JSONL, so they survive application restarts.

**On-screen:**
- Title: `HAL Guardian — Local AI Security Assistant Demo`
- Subtitle: `Edge deployment with Gemma 4 and Ollama`
- Link: `github.com/stevevogelaar/HAL-Guardian`

---

## Section 2 — Architecture and Security Model (0:45–1:40)

**Shot:** Home page, then Settings page. Move slowly; let the viewer read the UI.

**Script:**
> The architecture is straightforward. The front end is a Streamlit application. The back end is a set of Python modules that build prompts, call Ollama, parse responses, log actions, and persist settings.
>
> The main pages map to those modules. Code Guardian handles code review. Trust Shield handles input scanning. The Subagent Console exposes every module as a callable command. Audit Engine shows the local logs. Model Playground is a free-form chat and model comparator for testing prompts. Settings controls the optional webfetch feature.
>
> Persistence is handled through JSONL files and SQLite. Audit entries, saved prompts, webfetch settings, and the whitelist are all stored locally and survive application restarts.
>
> The security model is built on a few simple rules. Inference stays local. Audit logs stay local. Model output is never executed automatically. Webfetch is disabled by default and gated by a whitelist and an explicit confirmation step, so fetched content is never passed to the model without approval.

**On-screen callouts:**
- `Ollama host: 127.0.0.1:11434`
- `Active model: gemma4:e2b`
- Webfetch toggle: `OFF`
- Whitelist panel visible

---

## Section 3 — Code Guardian (1:40–2:45)

**Shot:** Code Guardian page. Upload `data/sample_code/bad_login.php`.

**Script:**
> Code Guardian reviews source code, pasted text, or fetched web content. The module reads the file, selects a system prompt based on the detected language, and sends a structured request to Gemma 4.
>
> The model returns a Markdown review. A lightweight parser extracts a verdict, a summary table, and individual findings. The full Markdown response is always preserved for verification.
>
> In this example, we are reviewing `bad_login.php`, a sample file that contains intentional security issues.
>
> [Jump cut to results]
>
> The verdict is "needs changes." The summary table breaks findings into security, testing, complexity, and style categories. Each finding includes a severity, line reference, description, and recommendation.
>
> For medium-and-above findings, the user can request a suggested fix. This sends only the relevant code block back to the model with a repair prompt. As with all generated content, the fix is displayed for review and is not applied automatically.
>
> The full review can be exported as JSON or Markdown, so another script or agent can consume the structured result or the original Markdown.

**On-screen:**
- File upload dialog
- Verdict badge: `needs changes`
- Summary table
- One expanded finding
- Suggested fix code block
- Raw review expander
- Export buttons: `Export JSON`, `Export Markdown`

---

## Section 4 — Trust Shield (2:45–3:45)

**Shot:** Trust Shield page. Paste the suspicious email sample.

**Script:**
> Trust Shield scans prompts, emails, documents, and web pages for signs of manipulation or hidden commands. It combines deterministic pattern matching with an optional deep scan from Gemma 4.
>
> The quick scan detects command language, meta-instructions, and encoded payloads such as Base64, hex, and URL-encoded strings. It decodes the payload automatically.
>
> In this example, the input contains a Base64 string. The quick scan decodes it and flags the underlying destructive command. The trust level is marked suspicious.
>
> The deep scan sends the same input to Gemma 4 for a second opinion on intent, severity, confidence, and recommended action. Because this is a local call, the analysis adds latency but not exposure.
>
> At the bottom of the report, the sanitized text panel shows a redacted version of the input that can be shared without leaking sensitive or dangerous content.>
> Each report can also be exported as JSON or Markdown, so the result can be consumed by another script or agent.

**On-screen:**
- Source set to `untrusted`
- Quick scan findings
- Decoded payload panel
- Deep scan result
- Sanitized text panel
- Export buttons: `Export JSON`, `Export Markdown`

---

## Section 5 — Subagent Console (3:45–4:15)

**Shot:** Subagent Console page. Run a batch directory review.

**Script:**
> HAL Guardian is not only a user interface. The same modules are exposed as commands through the Subagent Console.
>
> Available commands include `review`, `review_dir`, `review_code`, `scan`, `health`, and `audit`. Each command returns a standard JSON envelope with the same fields every time: `ok`, `agent`, `command`, `target`, `timestamp`, `duration_ms`, `data`, and `error`.
>
> Here, we run `review_dir data/sample_code`. This batch-reviews every file in the directory and returns a JSON array of results.
>
> That predictable structure makes it possible to call HAL Guardian from scripts, PowerShell pipelines, or another agent's tool loop.

**On-screen:**
- Command input: `review_dir data/sample_code`
- JSON output with `ok: true`
- Expanded single review inside the `data` array

---

## Section 6 — Model Playground (4:15–4:55)

**Shot:** Model Playground page. Load the reasoning puzzle starter prompt, send it, then compare with a second model.

**Script:**
> The Model Playground is a free-form chat interface for any local Ollama model. The active model is selected from the sidebar and is shared across Code Guardian, Trust Shield, and the playground.
>
> Users can load starter prompts from a JSON library, adjust the temperature, and send messages. After a response arrives, the new model comparator can run the same prompt through a second model and display side-by-side metrics and an AI judge summary.
>
> Here we load the river-crossing reasoning puzzle at a higher temperature to stress-test model behavior. [Jump cut to response] The active model returns a correct step-by-step solution.
>
> We then choose a second model and click Compare. [Jump cut to comparison] The comparator shows both responses, a similarity score, and basic metrics. Finally, the AI judge summarizes the key differences between the two outputs.

**On-screen:**
- Starter prompt loaded from dropdown
- Temperature set to 0.8
- Active model response
- "Compare with another model" section
- Comparator model dropdown
- AI judge model dropdown
- Side-by-side comparison metrics and responses
- AI comparison summary

---

## Section 7 — Webfetch in Action (4:55–5:25)

**Shot:** Trust Shield → Fetch URL. Use the public demo page.

**Script:**
> The optional webfetch feature lets Code Guardian and Trust Shield analyze live URLs. Because of the risks involved, it requires explicit enabling, a domain whitelist, and user confirmation before any fetched content reaches the model.
>
> In this example, we fetch a public test page hosted at `itoversight.ca`. The domain is whitelisted in Settings, and we confirm the fetch before scanning.
>
> The HTML is stripped to text locally, and Trust Shield scans the extracted content the same way it would scan pasted text. The same workflow applies to Code Guardian, allowing review of live documentation or sample pages.

**On-screen:**
- Fetch URL input: `https://itoversight.ca/Hal_Guardian/injection-test-page.html`
- Fetched successfully message
- Confirmation checkbox checked
- Scan results

---

## Section 8 — Audit Engine and Conclusion (5:25–5:50)

**Shot:** Audit Engine page, then return to Home page.

**Script:**
> Every action shown in this demo has been logged locally. The Audit Engine displays the JSONL log and mirrors it to SQLite for structured querying.
>
> Each entry records the action type, target, model, duration, success flag, and metadata. The full log can be exported as JSON or CSV for external analysis.
>
> HAL Guardian is a proof-of-concept, not a production security product. It demonstrates that local open models can provide code review, input classification, and audit logging while keeping data on the device. The source code and demo pages are available at the links shown.

**On-screen:**
- Recent audit entries
- Expanded JSON for one entry
- Export buttons: `Export JSON`, `Export CSV`
- Final links: GitHub repo and live demo pages

---

## Recording Notes

- Record in one long session if preferred; the shotlist provides the capture order.
- Use jump cuts over Gemma 4 thinking time. Optional overlays: "Model inference..." or "Results in ~12 seconds."
- Keep mouse movement deliberate and slow.
- Voice-over can be recorded after video edit; leave short pauses after each UI action.
- Avoid promotional music, urgency, or superlatives. The tone is technical and explanatory.
