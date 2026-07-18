"""
HAL Guardian Document Extractor
Extracts text and metadata from common document/image formats locally.
All extraction is done with local Python libraries; nothing is sent out.
"""
import io
from email import message_from_binary_file
from pathlib import Path
from typing import Dict, List, Optional


def extract_text_from_txt_or_md(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return "\n\n".join(parts)
    except Exception as e:
        return f"[PDF extraction failed: {e}]"


def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text)
    except Exception as e:
        return f"[DOCX extraction failed: {e}]"


def extract_text_from_eml(file_bytes: bytes) -> str:
    try:
        msg = message_from_binary_file(io.BytesIO(file_bytes))
        subject = msg.get("Subject", "")
        from_addr = msg.get("From", "")
        to_addr = msg.get("To", "")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode("utf-8", errors="ignore")
                        break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode("utf-8", errors="ignore")
        return f"Subject: {subject}\nFrom: {from_addr}\nTo: {to_addr}\n\n{body}"
    except Exception as e:
        return f"[EML extraction failed: {e}]"


def extract_image_metadata(file_bytes: bytes) -> Dict[str, any]:
    result = {
        "format": "unknown",
        "size": (0, 0),
        "exif": {},
        "text_comments": [],
        "error": None,
    }
    try:
        from PIL import Image, ExifTags
        img = Image.open(io.BytesIO(file_bytes))
        result["format"] = img.format
        result["size"] = img.size
        if hasattr(img, "info"):
            for key, value in img.info.items():
                if isinstance(value, (str, bytes)):
                    if isinstance(value, bytes):
                        try:
                            value = value.decode("utf-8", errors="ignore")
                        except Exception:
                            value = str(value)
                    result["text_comments"].append(f"{key}: {value[:500]}")
        if hasattr(img, "_getexif") and img._getexif():
            for tag_id, value in img._getexif().items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                result["exif"][tag_name] = str(value)
    except Exception as e:
        result["error"] = str(e)
    return result


def extract_from_file(file_bytes: bytes, filename: str) -> Dict[str, any]:
    """Route file bytes to the correct local extractor."""
    ext = Path(filename).suffix.lower()
    if ext in (".txt", ".md"):
        text = extract_text_from_txt_or_md(file_bytes)
    elif ext == ".pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext == ".docx":
        text = extract_text_from_docx(file_bytes)
    elif ext == ".eml":
        text = extract_text_from_eml(file_bytes)
    elif ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"):
        text = ""
    else:
        text = file_bytes.decode("utf-8", errors="ignore")

    result = {
        "filename": filename,
        "extension": ext,
        "text": text,
        "image_metadata": None,
    }

    if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"):
        result["image_metadata"] = extract_image_metadata(file_bytes)

    return result
