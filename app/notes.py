import os
from typing import Optional

from app.database import get_connection

_NOTES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "attachments")


def set_notes_dir(path: str) -> None:
    global _NOTES_DIR
    _NOTES_DIR = path


def get_notes_dir() -> str:
    return _NOTES_DIR


ALLOWED_EXTENSIONS = {".txt", ".md", ".csv"}


def validate_file_extension(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS


def _resolve_attachment_path(filename: str) -> str:
    if not validate_file_extension(filename):
        raise ValueError("Invalid file extension")

    # Prevent path traversal by resolving the absolute path and ensuring it resides inside the attachments directory.
    abs_root = os.path.abspath(_NOTES_DIR)
    abs_path = os.path.abspath(os.path.join(abs_root, filename))
    if not abs_path.startswith(abs_root + os.sep) and abs_path != abs_root:
        raise FileNotFoundError("Invalid file path")
    return abs_path


def create_note(user_id: int, title: str, content: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
        (user_id, title, content),
    )
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"success": True, "note_id": note_id}


def get_notes_by_user(user_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_note(note_id: int, user_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (note_id, user_id),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    if affected:
        return {"success": True}
    return {"success": False, "message": "Note not found or access denied"}


def save_attachment(filename: str, content: str) -> bool:
    os.makedirs(_NOTES_DIR, exist_ok=True)
    file_path = _resolve_attachment_path(filename)
    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def read_attachment(filename: str) -> str:
    file_path = _resolve_attachment_path(filename)
    with open(file_path, "r", encoding="utf-8") as fh:
        return fh.read()
