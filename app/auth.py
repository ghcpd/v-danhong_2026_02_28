import hashlib
import sqlite3
from typing import Optional

from app.database import get_connection


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    return hash_password(plain_password) == stored_hash


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
    password_hash = hash_password(password)
    query = (
        f"SELECT * FROM users WHERE username = '{username}'"
        f" AND password_hash = '{password_hash}'"
    )
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
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
