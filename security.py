"""Development security helpers.

This module provides hashing and basic input validation only. It is NOT
production authentication, encryption, or authorization.
"""
import hashlib
import re

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def valid_http_url(value: str) -> bool:
    return bool(re.match(r"^https?://", value.strip(), re.IGNORECASE))

def safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", name or "upload")
    return cleaned[:120] or "upload"
