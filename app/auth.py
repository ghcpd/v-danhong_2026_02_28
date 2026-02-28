import hashlib
import hmac
import os
import sqlite3
from typing import Optional

from app.database import get_connection


def hash_password(password: str) -> str:
    # Use PBKDF2-HMAC with sha256 and a random salt to produce a strong
    # password hash.  The returned string stores salt and digest separated
    # by a colon so we can verify later.
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt.hex() + ":" + dk.hex()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        salt_hex, dk_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        dk = bytes.fromhex(dk_hex)
    except ValueError:
        # malformed stored hash
        return False
    new_dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt, 100000)
    # constant-time comparison
    return hmac.compare_digest(new_dk, dk)


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
    # fetch the stored hash for this user and verify with verify_password
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
