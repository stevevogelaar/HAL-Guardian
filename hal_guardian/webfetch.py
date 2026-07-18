"""
HAL Guardian Webfetch
Safe, user-controlled web content fetching for Trust Shield and Code Guardian.

Controls:
- Master toggle (default OFF)
- Domain whitelist and blacklist stored in SQLite
- Max download size limit
- Allowed content types
- User confirmation before sending fetched content to LLM
"""
import re
from urllib.parse import urlparse
from typing import Dict, List, Optional, Tuple

import requests

from .memory import (
    get_webfetch_enabled,
    get_webfetch_max_size,
    get_webfetch_confirm,
    list_whitelist,
    list_blacklist,
)


def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower().strip()


def _is_allowed(url: str) -> Tuple[bool, str]:
    if not get_webfetch_enabled():
        return False, "Webfetch is disabled. Enable it in Settings."

    domain = _extract_domain(url)
    if not domain:
        return False, "Could not parse domain from URL."

    # Check blacklist first
    blacklist = {row["domain"] for row in list_blacklist()}
    if domain in blacklist or any(domain.endswith("." + d) or d.endswith("." + domain) for d in blacklist):
        return False, f"Domain '{domain}' is blacklisted."

    # Check whitelist
    whitelist = {row["domain"] for row in list_whitelist()}
    if domain in whitelist or any(domain.endswith("." + d) or d.endswith("." + domain) for d in whitelist):
        return True, ""

    return False, f"Domain '{domain}' is not in the whitelist. Add it in Settings."


def _allowed_content_type(content_type: str) -> bool:
    if not content_type:
        return False
    ct = content_type.lower()
    return any(t in ct for t in ["text/html", "text/plain", "application/json", "application/xhtml+xml"])


def fetch_url(url: str) -> Dict[str, any]:
    """
    Fetch a URL safely. Returns dict with keys: ok, url, error, status_code,
    content_type, size, text, domain.
    """
    allowed, reason = _is_allowed(url)
    if not allowed:
        return {"ok": False, "url": url, "error": reason}

    max_size = get_webfetch_max_size()
    try:
        with requests.get(url, timeout=15, stream=True, headers={"User-Agent": "HAL-Guardian/1.0"}) as r:
            content_type = r.headers.get("Content-Type", "")
            if not _allowed_content_type(content_type):
                return {"ok": False, "url": url, "error": f"Content type not allowed: {content_type}"}

            # Stream with size limit
            content = b""
            for chunk in r.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > max_size:
                    return {"ok": False, "url": url, "error": f"Download exceeded max size of {max_size} bytes"}

            text = content.decode("utf-8", errors="ignore")
            return {
                "ok": True,
                "url": url,
                "status_code": r.status_code,
                "content_type": content_type,
                "size": len(content),
                "text": text,
                "domain": _extract_domain(url),
            }
    except Exception as e:
        return {"ok": False, "url": url, "error": f"Fetch failed: {e}"}


def strip_html_to_text(raw_html: str) -> str:
    """Crude HTML-to-text extraction for scanning."""
    text = re.sub(r"\u003cscript[^\u003e]*\u003e.*?\u003c/script\u003e", " ", raw_html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\u003cstyle[^\u003e]*\u003e.*?\u003c/style\u003e", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\u003c[^\u003e]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_code_blocks(raw_html: str) -> List[str]:
    """Extract <code> and <pre> blocks from HTML."""
    blocks = []
    for tag in ["pre", "code"]:
        pattern = re.compile(rf"\u003c{tag}[^\u003e]*\u003e(.*?)\u003c/{tag}\u003e", re.DOTALL | re.IGNORECASE)
        for match in pattern.finditer(raw_html):
            text = re.sub(r"\u003c[^\u003e]+\u003e", "", match.group(1))
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                blocks.append(text)
    return blocks
