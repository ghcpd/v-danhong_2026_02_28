import hashlib
import hmac
import time
from typing import Optional

from app.config import JWT_SECRET, TOKEN_EXPIRY_SECONDS


def _compute_signature(payload: str) -> str:
    # Use HMAC with a secret key for signed tokens.
    return hmac.new(JWT_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


def generate_token(user_id: int) -> str:
    timestamp = str(int(time.time()))
    payload = f"{user_id}:{timestamp}"
    signature = _compute_signature(payload)
    return f"{payload}:{signature}"


def verify_token(token: str) -> dict:
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return {"valid": False, "reason": "malformed token"}
        user_id_str, timestamp_str, provided_sig = parts
        payload = f"{user_id_str}:{timestamp_str}"
        expected_sig = _compute_signature(payload)
        if not hmac.compare_digest(provided_sig, expected_sig):
            return {"valid": False, "reason": "invalid signature"}

        age = int(time.time()) - int(timestamp_str)
        if age > TOKEN_EXPIRY_SECONDS:
            return {"valid": False, "reason": "token expired"}
        return {"valid": True, "user_id": int(user_id_str)}
    except Exception:
        return {"valid": False, "reason": "error"}


def secure_compare(value_a: str, value_b: str) -> bool:
    return hmac.compare_digest(value_a, value_b)
