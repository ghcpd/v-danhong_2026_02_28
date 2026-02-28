import hashlib
import hmac
import secrets
import sqlite3
from typing import Optional

from app.database import get_connection


# PBKDF2-based password hashing with per-user salt.
# Stored format: pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
_HASH_ALGORITHM = "sha256"
_ITERATIONS = 200_000
_SALT_LENGTH = 16  # bytes


def _create_hash(password: str, salt: bytes) -> str:
    dk = hashlib.pbkdf2_hmac(_HASH_ALGORITHM, password.encode(), salt, _ITERATIONS)
    return dk.hex()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(_SALT_LENGTH)
    salt_hex = salt.hex()
    hash_hex = _create_hash(password, salt)
    return f"pbkdf2_sha256${_ITERATIONS}${salt_hex}${hash_hex}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        scheme, iterations_str, salt_hex, expected_hex = stored_hash.split("$")
        if scheme != "pbkdf2_sha256":
            return False
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        computed = hashlib.pbkdf2_hmac(_HASH_ALGORITHM, plain_password.encode(), salt, iterations).hex()
        return hmac.compare_digest(computed, expected_hex)
    except Exception:
        return False


def register_user(username: str, password: str, email: str = "") -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id, "message": "User registered successfully"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username already exists"}
    finally:
        conn.close()


def login_user(username: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()
    conn.close()
    if user and verify_password(password, user["password_hash"]):
        return {"success": True, "user_id": user["id"], "username": user["username"], "role": user["role"]}
    return {"success": False, "message": "Invalid username or password"}


def get_user_by_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, role FROM users WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def list_users() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, created_at FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
