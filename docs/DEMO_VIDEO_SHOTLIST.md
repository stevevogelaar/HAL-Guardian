# HAL Guardian — Demo Video Shotlist

**Final target length:** 3:30 – 4:50  
**Resolution:** 1920x1080 (record at 1080p or higher)  
**Frame rate:** 30fps  
**Audio:** Separate voice-over track, recorded after screen capture  
**Editing:** DaVinci Resolve; jump cuts allowed over model-thinking time

---

## Shot List

| # | Section | Visual | Approx. Final Time | Notes |
|---|---|---|---|---|
| 1 | Title card | Static title card with logo, tagline, GitHub link | 0:00–0:08 | Use project font; clean background |
| 2 | Fade to Home | HAL Guardian UI Home page | 0:08–0:35 | Show model selector and Ollama status; audio introduces safety framing |
| 3 | Settings page | Webfetch toggle OFF, whitelist empty, warning banner visible | 0:30–0:55 | Add `itoversight.ca` to whitelist on screen |
| 4 | Code Guardian setup | Mode: Upload a file; select `bad_login.php` | 0:55–1:10 | Keep file dialog visible briefly |
| 5 | Code Guardian review | Spinner / "Asking gemma4:e2b..." | 1:10–1:18 | Jump cut here; add "Results in ~12s" overlay if desired |
| 6 | Code Guardian results | Verdict, summary table, findings cards | 1:18–1:45 | Click one finding, then click Suggest fix |
| 7 | Code Guardian raw review | Expand "Raw review (Markdown)" | 1:45–1:55 | Short pan/scroll to show full response |
| 8 | Trust Shield setup | Paste suspicious email text, set source to `untrusted` | 1:55–2:08 | Use sample email from repo |
| 9 | Trust Shield quick scan | Results: trust level, decoded payload, findings | 2:08–2:22 | Highlight Base64 decode |
| 10 | Trust Shield deep scan | Enable deep scan, run, show model result | 2:22–2:40 | Jump cut over model thinking |
| 11 | Trust Shield sanitized text | Scroll to bottom, show redacted output | 2:40–2:50 | Pause for readability |
| 12 | Subagent Console | Type `review_dir data/sample_code`, run | 2:50–3:05 | Show JSON envelope result |
| 13 | Subagent Console details | Expand one review entry | 3:05–3:15 | Show structured data |
| 14 | Model Playground setup | Load starter prompt from dropdown | 3:15–3:22 | Show prompt text |
| 15 | Model Playground chat | Send prompt, show model response | 3:22–3:35 | Jump cut if response is slow |
| 16 | Model Playground save | Click Save, show prompt in saved list | 3:35–3:45 | Quick action |
| 17 | Webfetch Trust Shield | Switch to Fetch URL, enter demo URL | 3:45–3:52 | URL: `itoversight.ca/Hal_Guardian/injection-test-page.html` |
| 18 | Webfetch confirmation | Check "Proceed to scan" checkbox | 3:52–3:58 | Emphasize confirmation step |
| 19 | Webfetch scan results | Scan results for live page | 3:58–4:10 | Show it detected suspicious content |
| 20 | Audit Engine | Scroll recent entries | 4:10–4:25 | Expand one JSON entry |
| 21 | Home page return | Fade back to Home | 4:25–4:35 | Transition to outro |
| 22 | Outro title card | GitHub + live demo + license | 4:35–4:50 | Hold for final call-to-action |

---

## Suggested Jump-Cut Points

| Location | Reason | Suggested Overlay |
|---|---|---|
| Code Guardian after clicking review | Model inference time | "Gemma 4 thinking..." or fast-forward 2x |
| Trust Shield deep scan | Model inference time | "Deep scan in progress..." |
| Model Playground response | Model inference time | "Response in ~10s" |
| Subagent Console `review_dir` | Model inference time | "Batch review complete" |
| Webfetch scan | Combined fetch + model time | "Fetched and scanned" |

---

## DaVinci Resolve Timeline Tips

- **Track 1:** Screen recording footage
- **Track 2:** Title cards / lower thirds / callouts
- **Track 3:** Voice-over audio
- Use **Fusion** or **Text+** for simple lower thirds (model name, verdict, URLs)
- Export final as H.264 1080p for web upload

---

## Voice-Over Sync Notes

- Record voice-over after editing the video, or read script while capturing and replace later.
- Leave 0.3–0.5 second gaps after action clicks so the viewer can follow.
- When a model result appears, let the visual sit for 2–3 seconds before moving to the next line of narration.

---

## Required Files for Recording

- `data/sample_code/bad_login.php`
- `data/sample_inputs/suspicious_email.txt`
- `data/sample_code/` directory (for Subagent Console `review_dir`)
- Live URLs:
  - `https://itoversight.ca/Hal_Guardian/broken-code-page.html`
  - `https://itoversight.ca/Hal_Guardian/injection-test-page.html`
- Ollama running with `gemma4:e2b` pulled

---

## Backup Plan

If live model responses are too slow during recording:
1. Record the interactions as-is.
2. Use still frames of completed results and dissolve between them in Resolve.
3. Keep the audio script unchanged — the narration carries the story.
