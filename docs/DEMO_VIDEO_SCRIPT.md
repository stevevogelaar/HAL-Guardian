# HAL Guardian — Demo Video Script

**Target final length:** 3:30 – 4:30  
**Voice:** Friendly, direct, second-person — speak to the viewer.  
**Recording:** Screen capture of local Streamlit UI + separate voice-over in DaVinci Resolve.  
**Editing:** Jump cuts over model-thinking time; show results with optional "Results in X seconds" overlay.

---

## Section 1 — Hook (0:00–0:30)

**Shot:** Static title card with logo + tagline, then fade into the HAL Guardian UI on the Home page.

**Script:**
> What if you could get AI-powered code review and threat detection without ever sending your source code to the cloud?
>
> Meet HAL Guardian. It runs Google's Gemma 4 model entirely on your machine through Ollama. Your code, your prompts, your documents — they never leave your device unless you explicitly choose otherwise.
>
> In this demo, you'll see a full walkthrough of every module.

**On-screen:**
- Title: `HAL Guardian — Edge/On-Device AI Security Suite`
- Subtitle: `Built with Google Gemma 4 + Ollama`
- GitHub: `github.com/stevevogelaar/HAL-Guardian`

---

## Section 2 — Why Local First (0:30–0:55)

**Shot:** Home page showing Ollama status, active model dropdown, and recent activity snapshot.

**Script:**
> Right away, HAL Guardian shows you which local model is active and whether Ollama is reachable.
>
> This matters because most AI coding tools send your code to an API. HAL Guardian doesn't. Everything goes to `127.0.0.1:11434`. That is your local Ollama instance.
>
> Even the audit logs and saved settings live right here on your machine, in JSONL and SQLite.

**On-screen callout:**
- `Active model: gemma4:e2b`
- `Ollama status: reachable`
- `Logs: local only`

---

## Section 3 — Settings and Webfetch Safety (0:55–1:25)

**Shot:** Settings page. Show the webfetch toggle off by default, the whitelist, and the warning banner.

**Script:**
> Before we run any tools, let's talk about trust.
>
> HAL Guardian has an optional webfetch feature, but it is off by default. When it is on, it only allows whitelisted domains and asks for confirmation before sending fetched content to the model.
>
> This is a proof-of-concept, not enterprise isolation software. A live fetch can expose your IP, download malicious content, or reach internal services if the whitelist is misconfigured. So we keep the guardrails tight.
>
> For this demo, we'll use two public test pages hosted at itoversight.ca.

**On-screen:**
- Warning banner text visible
- `itoversight.ca` added to whitelist
- `Require confirmation before sending` checkbox checked

---

## Section 4 — Code Guardian (1:25–2:15)

**Shot:** Code Guardian page. Upload `data/sample_code/bad_login.php` and run the review.

**Script:**
> Now let's review some code.
>
> I'm uploading `bad_login.php`, a sample file with intentional security issues. HAL Guardian sends it to Gemma 4 locally and asks for a structured review.
>
> While the model thinks, you'll see a spinner. In the final edit we'll jump ahead to the results.
>
> [Jump cut to results]
>
> Here is the verdict: "needs changes." The summary table breaks issues down by category — security, testing, complexity, and style.
>
> Below that, each finding has severity, category, line reference, and a recommendation. And if you want a suggested fix, click the button. Gemma 4 will propose a safer version of that code block.
>
> The full raw Markdown review is always preserved, so you can verify what the model actually said.

**On-screen:**
- Verdict badge
- Summary table with non-zero counts
- One "Suggest fix" expanded
- Raw review (Markdown) expander visible

---

## Section 5 — Trust Shield (2:15–2:55)

**Shot:** Trust Shield page. Paste content from `data/sample_inputs/suspicious_email.txt` and run a deep scan.

**Script:**
> Next, Trust Shield. This module protects you from prompt injection and hidden payloads.
>
> I'll paste a suspicious email that contains encoded commands. The quick scan runs instantly and flags command language, meta-instructions, and a Base64 payload.
>
> Then I enable the deep scan and ask Gemma 4 for a second opinion. It returns a trust level, confidence score, and recommended action.
>
> At the bottom you also get a sanitized version of the input, so you can share a redacted copy safely.

**On-screen:**
- Quick scan findings
- Decoded Base64 payload revealed
- Deep scan result: trust level = suspicious
- Sanitized text panel

---

## Section 6 — Subagent Console (2:55–3:20)

**Shot:** Subagent Console page. Type `review_dir data/sample_code` and run it.

**Script:**
> HAL Guardian isn't just a UI. Every module is exposed as a subagent command.
>
> Here in the Subagent Console, I can run `review_dir data/sample_code` and batch-review every file in that folder.
>
> The result is a standard JSON envelope. That means scripts, PowerShell pipelines, or another AI agent can call HAL Guardian as a tool and consume the output predictably.

**On-screen:**
- Command input
- JSON result with `ok: true`, `agent: code_guardian`, and list of reviews

---

## Section 7 — Model Playground (3:20–3:45)

**Shot:** Model Playground page. Load a starter prompt, send it, and save it.

**Script:**
> The Model Playground is a free-form chat with any local Ollama model.
>
> You can load a starter prompt, tune temperature, or just experiment. If you find a prompt you want to keep, click Save and it goes into the SQLite-backed prompt library.

**On-screen:**
- Starter prompt loaded
- Model response
- Save button clicked, prompt appears in saved list

---

## Section 8 — Webfetch in Action (3:45–4:15)

**Shot:** Trust Shield → Fetch URL. Use `https://itoversight.ca/Hal_Guardian/injection-test-page.html`. Confirm, then scan.

**Script:**
> Now let's see webfetch in action.
>
> In Trust Shield I switch the input mode to Fetch URL and paste our public demo page. The page simulates a malicious email hosted on the web.
>
> Because I whitelisted this domain and confirmed the fetch, HAL Guardian downloads the HTML, extracts the text, and passes it to the scan.
>
> The same workflow works in Code Guardian, so you can review live documentation or bug-report pages as easily as local files.

**On-screen:**
- URL entered
- Fetched successfully message
- Confirmation checkbox
- Scan results for the live page

---

## Section 9 — Audit Engine (4:15–4:35)

**Shot:** Audit Engine page. Scroll through recent actions from the demo.

**Script:**
> Everything we just did was logged locally.
>
> The Audit Engine shows every action: what was reviewed, which model was used, how long it took, and whether it succeeded. This makes HAL Guardian accountable and easy to debug.

**On-screen:**
- List of recent entries
- JSON details expanded for one entry

---

## Section 10 — Outro (4:35–4:50)

**Shot:** Return to Home page, then fade to title card.

**Script:**
> HAL Guardian proves that local open models can deliver real security value without sacrificing privacy.
>
> It is built with Google Gemma 4, runs through Ollama, and is open source under Apache 2.0.
>
> Try it yourself at the GitHub link on screen. Thanks for watching.

**On-screen:**
- `github.com/stevevogelaar/HAL-Guardian`
- `itoversight.ca/Hal_Guardian/`
- `Apache 2.0`

---

## Recording Notes

- Record in one long session if you prefer. The shotlist above gives the order and what to capture.
- Use jump cuts over spinner delays. Optional overlay: "Model thinking... 14 seconds" or fast-forward with timecode.
- Keep mouse movements slow and deliberate for clarity.
- Speak the script naturally; you can rephrase to sound more human as long as the key points remain.
- Target final audio length: 3:30–4:30. Visuals can extend slightly during results screens.
