# HAL Guardian — Educational Demo Video Shotlist

**Project type:** Local proof-of-concept AI security assistant  
**Tone:** Educational technical demo  
**Final target length:** 4:00 – 5:40  
**Resolution:** 1920x1080 or higher  
**Frame rate:** 30fps  
**Audio:** Separate voice-over track, recorded after video edit  
**Editing:** DaVinci Resolve; jump cuts over model inference are expected

---

## Shot List

| # | Section | Visual | Approx. Final Time | Notes |
|---|---|---|---|---|
| 1 | Title card | Static title card with project name and subtitle | 0:00–0:10 | Neutral typography; no sales language |
| 2 | Home page | HAL Guardian UI Home page; model status visible | 0:10–0:45 | Let viewer absorb the local-only framing |
| 3 | Settings page | Webfetch toggle OFF; whitelist and warning visible | 0:45–1:10 | Move slowly; call out security model |
| 4 | Architecture diagram | Optional static diagram of module layout | 1:10–1:40 | Can be skipped if narration is clear |
| 5 | Code Guardian setup | Upload `bad_login.php`; select PHP language | 1:40–1:55 | Show file path in dialog |
| 6 | Code Guardian thinking | Spinner / "Asking gemma4:e2b..." | 1:55–2:02 | Jump cut here |
| 7 | Code Guardian results | Verdict, summary table, findings cards | 2:02–2:25 | Click one finding |
| 8 | Code Guardian suggest fix | Expanded suggested fix block | 2:25–2:40 | Show replacement code |
| 9 | Code Guardian export | Hover or click Export JSON / Markdown buttons | 2:40–2:48 | Show both options |
| 10 | Code Guardian raw review | Expand raw Markdown review | 2:48–2:52 | Brief scroll |
| 10 | Trust Shield setup | Paste suspicious email; set source `untrusted` | 2:45–3:00 | Use repo sample input |
| 11 | Trust Shield quick scan | Findings and decoded payload | 3:00–3:15 | Highlight the Base64 decode |
| 12 | Trust Shield deep scan | Enable deep scan; show model result | 3:15–3:30 | Jump cut here |
| 13 | Trust Shield export | Hover or click Export JSON / Markdown buttons | 3:30–3:38 | Show both options |
| 14 | Trust Shield sanitized text | Bottom panel with redacted input | 3:38–3:45 | Pause for readability |
| 14 | Subagent Console setup | Command input `review_dir data/sample_code` | 3:45–3:55 | Show typing |
| 15 | Subagent Console results | JSON envelope returned | 3:55–4:05 | Jump cut here |
| 16 | Subagent Console details | Expand one review entry | 4:05–4:15 | Show structured fields |
| 17 | Model Playground setup | Load starter prompt from dropdown | 4:15–4:25 | Show prompt text |
| 18 | Model Playground response | Model output visible | 4:25–4:35 | Jump cut if needed |
| 19 | Model Playground save | Save prompt; show persisted list | 4:35–4:42 | Quick action |
| 20 | Model Playground export | Hover or click Export prompt library (JSON) button | 4:42–4:48 | Show JSON export option |
| 20 | Webfetch setup | Trust Shield → Fetch URL; enter demo URL | 4:45–4:55 | URL: `itoversight.ca/Hal_Guardian/injection-test-page.html` |
| 21 | Webfetch confirmation | Check proceed checkbox | 4:55–5:00 | Emphasize confirmation gate |
| 22 | Webfetch scan results | Scan results for fetched page | 5:00–5:15 | Jump cut over fetch + model time |
| 23 | Audit Engine | Scroll recent entries; expand one JSON object | 5:15–5:28 | Show local logging |
| 24 | Audit Engine export | Hover or click Export JSON / CSV buttons | 5:28–5:36 | Show both options |
| 25 | Home return / conclusion | Fade back to Home page | 5:36–5:45 | Final links visible |

---

## Suggested Jump-Cut Points

| Location | Reason | Suggested Overlay |
|---|---|---|
| Code Guardian review | Gemma 4 inference | "Model inference..." or fast-forward |
| Trust Shield deep scan | Gemma 4 inference | "Deep scan inference..." |
| Subagent Console `review_dir` | Batch Gemma 4 inference | "Batch review complete" |
| Model Playground response | Gemma 4 inference | "Response in ~10s" |
| Webfetch scan | Network fetch + inference | "Fetched and analyzed" |

---

## DaVinci Resolve Timeline Structure

| Track | Content |
|---|---|
| Video 1 | Screen recording footage |
| Video 2 | Title cards and lower-third callouts |
| Audio 1 | Voice-over narration |
| Audio 2 | Optional quiet system/UI clicks (very low) |

- Use **Text+** for lower thirds: model names, verdicts, URLs.
- Avoid flashy transitions. Simple cuts or short dissolves only.
- Export as H.264 1080p for web upload.

---

## Voice-Over Sync Notes

- Record narration after picture lock for clean audio.
- Leave 0.3–0.5 second gaps after each click or major UI change.
- Hold on result screens for 2–3 seconds before moving to the next narration point.
- Read at a measured pace; avoid upspeak or promotional inflection.

---

## Assets Needed for Recording

- HAL Guardian running with Ollama and `gemma4:e2b` available
- `data/sample_code/bad_login.php`
- `data/sample_inputs/suspicious_email.txt`
- `data/sample_code/` directory
- Live URLs reachable:
  - `https://itoversight.ca/Hal_Guardian/broken-code-page.html`
  - `https://itoversight.ca/Hal_Guardian/injection-test-page.html`
- Whitelist pre-configured with `itoversight.ca` if desired

---

## Backup Plan

If model responses are too slow during a single recording session:
1. Capture all interactions as-is.
2. In Resolve, hold on the completed-result frames and dissolve between them.
3. Keep narration continuous; the audio tells the story while the visuals show evidence.
