import hashlib
import hmac
import secrets
import sqlite3
from typing import Optional

from app.database import get_connection


def hash_password(password: str) -> str:
    # Use PBKDF2-HMAC-SHA256 with a random salt to securely hash passwords.
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    # Encode as hex for storage: salt + hash
    return f"{salt.hex()}${dk.hex()}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        salt_hex, hash_hex = stored_hash.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        derived = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100_000)
        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(derived, expected_hash)
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
    # Use parameterized queries to prevent SQL injection.
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
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
