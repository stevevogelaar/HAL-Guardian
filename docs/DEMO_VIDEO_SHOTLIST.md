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
| 3 | Sidebar active model | Show Active model dropdown under Choose a module | 0:45–0:55 | Mention it drives Code Guardian, Trust Shield, and Model Playground |
| 4 | Settings page | Webfetch toggle OFF; whitelist and warning visible | 0:55–1:15 | Move slowly; call out security model |
| 5 | Architecture diagram | Optional static diagram of module layout | 1:15–1:40 | Can be skipped if narration is clear |
| 6 | Code Guardian setup | Upload `bad_login.php`; select PHP language | 1:40–1:55 | Show file path in dialog |
| 7 | Code Guardian thinking | Spinner / "Asking gemma4:e2b..." | 1:55–2:02 | Jump cut here |
| 8 | Code Guardian results | Verdict, summary table, findings cards | 2:02–2:25 | Click one finding |
| 9 | Code Guardian suggest fix | Expanded suggested fix block | 2:25–2:40 | Show replacement code |
| 10 | Code Guardian export | Hover or click Export JSON / Markdown buttons | 2:40–2:48 | Show both options |
| 11 | Code Guardian raw review | Expand raw Markdown review | 2:48–2:52 | Brief scroll |
| 12 | Trust Shield setup | Paste suspicious email; set source `untrusted` | 2:52–3:05 | Use repo sample input |
| 13 | Trust Shield quick scan | Findings and decoded payload | 3:05–3:18 | Highlight the Base64 decode |
| 14 | Trust Shield deep scan | Enable deep scan; show model result | 3:18–3:30 | Jump cut here |
| 15 | Trust Shield export | Hover or click Export JSON / Markdown buttons | 3:30–3:38 | Show both options |
| 16 | Trust Shield sanitized text | Bottom panel with redacted input | 3:38–3:45 | Pause for readability |
| 17 | Subagent Console setup | Command input `review_dir data/sample_code` | 3:45–3:55 | Show typing |
| 18 | Subagent Console results | JSON envelope returned | 3:55–4:05 | Jump cut here |
| 19 | Subagent Console details | Expand one review entry | 4:05–4:15 | Show structured fields |
| 17 | Model Playground setup | Load reasoning puzzle starter prompt from dropdown; set temperature 0.8 | 4:15–4:25 | Show prompt text |
| 18 | Model Playground response | Active model response visible | 4:25–4:35 | Jump cut if needed |
| 19 | Model Playground compare | Select comparator model and click Compare | 4:35–4:45 | Excludes active model from dropdown |
| 20 | Model Playground comparison | Side-by-side metrics and responses | 4:45–4:55 | Show similarity score |
| 21 | Model Playground AI judge | Click AI compare; show judge summary | 4:55–5:05 | Jump cut over judge inference |
| 22 | Model Playground export | Hover or click Export comparison (JSON) button | 5:05–5:12 | Show JSON export option |
| 23 | Webfetch setup | Trust Shield → Fetch URL; enter demo URL | 5:12–5:20 | URL: `itoversight.ca/Hal_Guardian/injection-test-page.html` |
| 24 | Webfetch confirmation | Check proceed checkbox | 5:20–5:25 | Emphasize confirmation gate |
| 25 | Webfetch scan results | Scan results for fetched page | 5:25–5:38 | Jump cut over fetch + model time |
| 26 | Audit Engine | Scroll recent entries; expand one JSON object | 5:38–5:48 | Show local logging |
| 27 | Audit Engine export | Hover or click Export JSON / CSV buttons | 5:48–5:55 | Show both options |
| 28 | Home return / conclusion | Fade back to Home page | 5:55–6:05 | Final links visible |

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
