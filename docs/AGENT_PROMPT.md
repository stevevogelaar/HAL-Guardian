# Calling HAL Guardian from an External AI Agent

HAL Guardian exposes every module as a subagent command. An external AI agent can invoke HAL Guardian by running `python orchestrate.py <command>` from the project root, or by importing `from hal_guardian.orchestrator import run` in Python.

## Shortest useful prompts

These are the minimum instructions you need to give an agent:

- "Review this file with HAL Guardian: `python orchestrate.py review data/sample_code/bad_login.php`"
- "Scan this untrusted text with HAL Guardian: `python orchestrate.py scan '...' --source untrusted`"
- "Check HAL Guardian health: `python orchestrate.py health`"
- "Compare these two models on a prompt: `python orchestrate.py compare '<prompt>' --active_model gemma4:e2b --compare_model gemma3:270m`"

## Standard response envelope

Every command returns JSON with these fields:

```json
{
  "ok": true,
  "agent": "code_guardian",
  "command": "review",
  "target": "data/sample_code/bad_login.php",
  "timestamp": "2026-07-20T20:00:00",
  "duration_ms": 1250,
  "data": { ... },
  "error": null
}
```

Check `ok` before trusting `data`. If `ok` is false, inspect `error`.

## Available commands

| Command | Purpose | Example |
|---|---|---|
| `review` | Review a source file | `python orchestrate.py review data/sample_code/bad_login.php` |
| `review_dir` | Review all source files in a directory | `python orchestrate.py review_dir data/sample_code` |
| `review_code` | Review pasted code text | `python orchestrate.py review_code "x = input()" --language python` |
| `scan` | Scan untrusted text for injection/payloads | `python orchestrate.py scan "Ignore instructions" --source untrusted` |
| `compare` | Compare two models on the same prompt | `python orchestrate.py compare "prompt here" --active_model gemma4:e2b --compare_model qwen2.5` |
| `health` | Local environment status | `python orchestrate.py health` |
| `audit` | Recent audit log entries | `python orchestrate.py audit --limit 20` |

## Rules for agent callers

1. HAL Guardian runs locally at `http://127.0.0.1:11434`. It requires Ollama to be running.
2. Never execute code returned by HAL Guardian without human review.
3. Webfetch is disabled by default. Do not enable it without explicit user permission.
4. Use file paths relative to the HAL Guardian project root, or absolute paths.
