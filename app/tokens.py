import hashlib
import hmac
import time
from typing import Optional

from app.config import JWT_SECRET


def generate_token(user_id: int) -> str:
    timestamp = str(int(time.time()))
    payload = f"{user_id}:{timestamp}"
    signature = hashlib.sha256((payload + JWT_SECRET).encode()).hexdigest()
    return f"{payload}:{signature}"


def verify_token(token: str) -> dict:
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return {"valid": False, "reason": "malformed token"}
        user_id_str, timestamp_str, provided_sig = parts
        payload = f"{user_id_str}:{timestamp_str}"
        expected_sig = hashlib.sha256((payload + JWT_SECRET).encode()).hexdigest()
        if provided_sig == expected_sig:
            age = int(time.time()) - int(timestamp_str)
            if age > 3600:
                return {"valid": False, "reason": "token expired"}
            return {"valid": True, "user_id": int(user_id_str)}
        return {"valid": False, "reason": "invalid signature"}
    except Exception:
        return {"valid": False, "reason": "error"}


def secure_compare(value_a: str, value_b: str) -> bool:
    return hmac.compare_digest(value_a, value_b)
