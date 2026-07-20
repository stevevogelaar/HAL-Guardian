# HAL Guardian — Hackathon Submission Checklist

## Event: GDG Windsor Build with AI — Gemma Hackathon 2026
## Track: Edge / On-Device
## Team: HAL Guardian (Steve Vogelaar + AI collaborator)
## License: Apache 2.0
## Deadline: July 24, 2026

---

## Submission Requirements

| Requirement | Status | Notes |
|---|---|---|
| **GitHub repository** | ✅ Ready | `https://github.com/stevevogelaar/HAL-Guardian.git` |
| **Writeup / description** | ✅ Ready | `docs/HACKATHON_WRITEUP.md` polished |
| **Demo video** | ⏳ Pending | 2-3 minutes, screen recording + narration (Steve to record) |
| **Live demo pages** | ✅ Ready | `https://itoversight.ca/Hal_Guardian/` |
| **Code runs locally** | ✅ Verified | Streamlit + Ollama, no cloud dependency |

---

## Pre-Submission Tasks

### Writeup Polish
- [x] Review `hackathon_writeup[DRAFT-02].md` for accuracy (model names, URLs, features)
- [x] Ensure Gemma 4 references are correct (not old Gemma 2/3 names)
- [x] Add paragraph on "Why Edge/On-Device matters" (privacy, cost, compliance)
- [x] Final proofread: grammar, clarity, technical accuracy
- [ ] Rename to `HACKATHON_WRITEUP_FINAL.md` (Steve to decide if final lives in repo)

### Demo Video
- [ ] Script narration (2-3 minutes max)
- [ ] Record screen: Code Guardian reviewing broken-code-page.html
- [ ] Record screen: Trust Shield scanning injection-test-page.html
- [ ] Record screen: Model Playground chatting with Gemma 4
- [ ] Show local-only operation (no API keys, no cloud calls)
- [ ] Upload to YouTube or Vimeo (unlisted is fine)
- [ ] Add video link to writeup + GitHub README

### Model Playground Enhancement
- [x] Add multi-model comparator: active model vs any other loaded model on same prompt
- [x] Metrics: latency (ms), response length, estimated tokens/sec, similarity score
- [x] AI judge summary comparing the two responses
- [x] Persistent recall via SQLite comparison history
- [x] JSON export for each comparison
- [ ] Screenshot the comparison table for writeup (Steve to record demo)

### Code Freeze & Verification
- [ ] Tag final commit: `git tag -a hackathon-submission -m "Gemma Hackathon 2026 submission"`
- [ ] Push tag to GitHub: `git push origin hackathon-submission`
- [x] Python syntax check passed for all modified files
- [ ] Test fresh clone on clean machine:
  ```powershell
  git clone https://github.com/stevevogelaar/HAL-Guardian.git
  cd HAL-Guardian
  python -m pip install -r requirements.txt
  python -m streamlit run app.py
  ```
- [ ] Verify all demo pages load and analyze correctly

### Submission Form
- [ ] Confirm event submission URL (GDG Windsor / DevPost / Google form)
- [ ] Fill out team info: Steve Vogelaar + AI collaborator
- [ ] Paste GitHub repo link
- [ ] Paste writeup (or link to `HACKATHON_WRITEUP_FINAL.md`)
- [ ] Paste demo video URL
- [ ] Confirm track: Edge / On-Device
- [ ] Submit before deadline

---

## Post-Submission

- [ ] Share submission on LinkedIn / Twitter
- [ ] Update `README.md` with "Hackathon Submission" badge
- [ ] Archive writeup + video to `_HAL/memory/hackathons/2026-07-gemma/`
- [ ] Celebrate — then get back to server migration 😄

---

## Resources

| File | Path | Purpose |
|------|------|---------|
| Draft writeup | `docs/hackathon_writeup[DRAFT-02].md` | 906 words, needs polish |
| Final writeup | `docs/HACKATHON_WRITEUP.md` | Current best version (may be outdated) |
| Demo shotlist | `docs/DEMO_VIDEO_SHOTLIST.md` | What to record |
| Demo script | `docs/DEMO_VIDEO_SCRIPT.md` | Narration script |
| Architecture | `docs/ARCHITECTURE.md` | Technical reference |
| Live pages | `https://itoversight.ca/Hal_Guardian/` | Test targets |
| Repo | `https://github.com/stevevogelaar/HAL-Guardian.git` | Submission link |

---

## Changelog

- **2026-07-19**: Created from server checklist Phase 5. Extracted hackathon tasks to dedicated file.
