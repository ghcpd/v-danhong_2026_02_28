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
    # ensure the target path stays within the attachments directory
    os.makedirs(_NOTES_DIR, exist_ok=True)
    file_path = os.path.join(_NOTES_DIR, filename)
    normalized = os.path.realpath(file_path)
    if not normalized.startswith(os.path.realpath(_NOTES_DIR) + os.sep):
        raise ValueError("Invalid attachment path")
    with open(normalized, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def read_attachment(filename: str) -> str:
    file_path = os.path.join(_NOTES_DIR, filename)
    normalized = os.path.realpath(file_path)
    if not normalized.startswith(os.path.realpath(_NOTES_DIR) + os.sep):
        # prevent directory traversal
        raise FileNotFoundError("Invalid attachment path")
    with open(normalized, "r", encoding="utf-8") as fh:
        return fh.read()
