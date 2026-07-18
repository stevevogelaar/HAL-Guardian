"""
HAL Guardian configuration.
"""
import os

# Ollama settings
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.environ.get("HAL_GUARDIAN_MODEL", "gemma4:e2b")
FAST_MODEL = "gemma4:e2b"
REVIEW_MODEL = "gemma4:e2b"  # Can be upgraded to gemma4:4b if available


def get_available_models() -> list:
    """Query Ollama for locally pulled model names."""
    try:
        import requests
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        if r.ok:
            return [m.get("name") for m in r.json().get("models", []) if m.get("name")]
    except Exception:
        pass
    return [DEFAULT_MODEL]

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_PATH = os.path.join(PROJECT_ROOT, "audits", "hal-guardian-audit.jsonl")
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "hal_guardian", "prompts")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Review limits
MAX_PROMPT_CHARS = 24000
COMPACT_PROMPT_CHARS = 6000
MAX_FILE_CHARS = 30000
OLLAMA_TIMEOUT = 180

# UI
APP_TITLE = "HAL Guardian — Local AI Security Suite"
APP_ICON = "🛡️"
