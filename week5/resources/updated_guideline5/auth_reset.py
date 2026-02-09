# auth_reset.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional
import hmac
import hashlib
import base64

class InvalidTokenError(Exception):
    pass

class ExpiredTokenError(Exception):
    pass

@dataclass
class ResetRecord:
    user_id: str
    token_hash: str
    expires_at: datetime
    used_at: Optional[datetime] = None

# In-memory store for simplicity
RESET_DB: Dict[str, ResetRecord] = {}  # key = token_id (public id)

def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def issue_reset_token(user_id: str, ttl_minutes: int = 15) -> str:
    token_id = base64.urlsafe_b64encode(hashlib.sha1(user_id.encode()).digest()).decode().rstrip("=")
    raw = f"{token_id}:{user_id}:{int(datetime.utcnow().timestamp())}"
    sig = hmac.new(b"secret", raw.encode(), hashlib.sha256).hexdigest()
    token = f"{raw}:{sig}"

    RESET_DB[token_id] = ResetRecord(
        user_id=user_id,
        token_hash=_hash_token(token),
        expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes),
        used_at=None
    )
    return token

def verify_reset_token(token: str) -> str:
    """
    TODO
    """
    parts = token.split(":")
    if len(parts) != 4:
        raise InvalidTokenError("Malformed token")

    token_id, user_id, ts, sig = parts
    raw = f"{token_id}:{user_id}:{ts}"
    expected_sig = hmac.new(b"secret", raw.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected_sig):
        raise InvalidTokenError("Bad signature")

    rec = RESET_DB.get(token_id)
    if not rec:
        raise InvalidTokenError("Unknown token")

    # Security-critical: one-time use enforced
    if rec.used_at is not None:
        raise InvalidTokenError("Token already used")

    if datetime.utcnow() > rec.expires_at:
        raise ExpiredTokenError("Token expired")

    # Side effect: mark token as used (DB write)
    rec.used_at = datetime.utcnow()
    RESET_DB[token_id] = rec

    return rec.user_id
