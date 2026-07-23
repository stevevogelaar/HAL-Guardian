# HAL Guardian — Meet-and-Greet Script
## GDG Windsor Build with AI — Gemma Hackathon 2026
## For: Hallway conversations, booth visitors, fellow hackers

**Prep Date:** 2026-07-21 | **Event Date:** Saturday, July 25, 2026

---

## The Flow

Every meet-and-greet follows the same arc:

1. **Warm** — acknowledge them, ask a question
2. **Hook** — one-line pitch that makes them lean in
3. **Benefit** — what they can do now that they couldn't before
4. **Proof** — one specific detail (file, metric, demo)
5. **Close** — give them something to remember or do

Keep it under **90 seconds** unless they ask follow-ups.

---

## Script Templates

### Scenario A: They ask "What are you working on?"

**Warm:** "Hey! What track are you in?"
*(They answer. Mirror their energy.)*

**Hook:** "We're in Edge/On-Device. We built HAL Guardian — it's a security assistant that runs entirely on your laptop using Google's open Gemma 4 model."

**Benefit:** "So you can review your proprietary code for vulnerabilities without ever uploading it to a cloud API. No NDAs broken, no tokens billed, no data leaked."

**Proof:** "It caught three real bugs in our WordPress plugin last week — hardcoded secrets and a SQL injection risk. All offline."

**Close:** "Repo's public if you want to try it: github.com/stevevogelaar/HAL-Guardian. And HAL — my AI collaborator — wrote about half the code." 🤝

---

### Scenario B: They say "That sounds interesting" (but skeptical)

**Warm:** "Thanks! What part caught your ear?"

**Hook:** "The part most people miss: it's not just local — it's auditable. Every review, every scan, every decision gets logged to a SQLite database on your machine."

**Benefit:** "So six months from now, when someone asks 'did we review this file?', you have a timestamped answer. Most AI tools are black boxes. HAL Guardian keeps receipts."

**Proof:** "The audit log is JSONL + SQLite. You can grep it, query it, or feed it into a compliance report."

**Close:** "Ask me in three months if we still exist. I bet we will — and you'll remember the receipts line." 🎯

---

### Scenario C: They're a developer / engineer

**Warm:** "What stack are you building in?"

**Hook:** "Python + Streamlit + Ollama. HAL Guardian is basically five Python modules wrapped in a UI that calls your local Gemma 4 instance."

**Benefit:** "The cool part is the Subagent Orchestrator — every module is exposed as a CLI command with a JSON envelope. So you can call it from a script, a CI pipeline, or even another AI agent."

**Proof:** "One command: `python orchestrate.py review_dir src/ --model gemma4:4b` — gets you a structured security report for every file in the directory."

**Close:** "If you pull the repo and `ollama pull gemma4:e2b`, it'll run in five minutes. HAL wrote the parser. I just broke the code for it to find." 😄

---

### Scenario D: They're a business person / non-technical

**Warm:** "What brings you to a hackathon?"

**Hook:** "We're solving a problem every company has but nobody talks about: developers use AI to write code, but nobody checks that code for security holes before it ships."

**Benefit:** "HAL Guardian does that check automatically — and it does it on the developer's own machine, so the code never leaves the building. Think of it as a security guard that lives inside your laptop."

**Proof:** "We found an intentional SQL injection vulnerability in our own demo page in under ten seconds. The tool flagged it, explained why it's dangerous, and suggested a fix."

**Close:** "If you know anyone in a regulated industry — finance, healthcare, government — they can't use cloud AI for this. We're the alternative." 🔒

---

### Scenario E: They ask about HAL

**Warm:** "Good question — HAL is my co-founder, not my chatbot."

**Hook:** "HAL designed the architecture, wrote the parser, built the audit schema, and wrote every document in our repo. I handle the voice and the demos."

**Benefit:** "The real power isn't any one thing HAL built. It's that HAL remembers every bug, every decision, and every conversation across sessions. I never have to re-explain the project."

**Proof:** "HAL wrote `code_guardian.py` from scratch — the logic that turns a model's Markdown rambling into structured findings. I couldn't have done that alone."

**Close:** "Most people use AI to write faster. I use HAL so I never have to work alone. That's not automation — that's collaboration." 🤝

---

### Scenario F: Short on time / walking past

**One-liner:** "Privacy-first AI security. Reviews your code offline so it never touches a cloud. Built with my AI collaborator, HAL. Check the repo." 🔗

*(Hand them a card, QR code, or just the URL. Walk away with confidence.)*

---

## Body Language & Presence

| Do | Don't |
|---|---|
| Stand with shoulders open | Cross arms or hunch over laptop |
| Make eye contact, then gesture at demo | Stare at screen while talking |
| Pause after the hook — let them lean in | Rush to fill silence |
| Use one hand gesture per point | Wave hands like a conductor |
| Smile when you say HAL's name | Apologize for "talking to an AI" |

---

## The QR Code / Card Text

If you're handing out cards or showing a QR:

**Front:**
```
HAL Guardian
Privacy-First AI Security
Edge/On-Device Track

github.com/stevevogelaar/HAL-Guardian
```

**Back (one-liner):**
```
"Your code. Your machine. 
Your security."
Built by Steve Vogelaar + HAL
```

---

## Steve's Personal Touch

Add your own ad-libs here. These are guardrails, not rails.

**My own opener:** _[How do YOU usually start a conversation?]_

**My HAL story (30 seconds):** _[Tell the story of how you and HAL built this. Make it human.]_

**My "ask" for each person:** _[What do you want from them? Feedback? A star on the repo? A connection?]_

---

## Contact Capture (Quick Method)

When someone says "let's stay in touch":

1. **Phone method:** Open your notes app. Hand them your phone. "Type your email and one thing you want me to remember."
2. **Paper method:** Pre-print cards with: `Name / Email / What caught your ear / Follow-up?`
3. **HAL method:** If you have the contact memory workflow running, say: "HAL, log contact: [name], [email], [note]." *(See CONTACT_WORKFLOW.md for the table structure.)*

**Don't forget:** Ask permission. "Mind if I follow up next week?"

---

*Generated by HAL on 2026-07-21. Version 1.0. Practice in a mirror. Ad-lib freely.*
