import os
import pytest


@pytest.fixture(autouse=True)
def isolated_database(tmp_path):
    """Redirect the database and attachments directory to a temporary location for each test."""
    from app import database, notes

    db_file = str(tmp_path / "test_securevault.db")
    attachments_dir = str(tmp_path / "attachments")

    database.set_db_path(db_file)
    notes.set_notes_dir(attachments_dir)

    database.init_db()
    os.makedirs(attachments_dir, exist_ok=True)

    yield

    # tmp_path is cleaned up automatically by pytest
