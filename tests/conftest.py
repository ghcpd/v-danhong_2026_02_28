import os
import pytest


def pytest_configure(config):
    """Set environment variables before test collection."""
    os.environ["SECRET_KEY"] = "secure_test_secret_key_12345"
    os.environ["JWT_SECRET"] = "secure_test_jwt_secret_key"
    os.environ["ADMIN_PASSWORD"] = "SecureTestPassword123!"


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
