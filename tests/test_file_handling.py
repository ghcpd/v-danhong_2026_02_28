"""Tests targeting file-handling security vulnerabilities, including path traversal."""

import os

import pytest

from app.notes import (
    get_notes_dir,
    read_attachment,
    save_attachment,
    validate_file_extension,
)


def test_file_extension_validation():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/notes.py - validate_file_extension()
    Fix hint: No fix needed; confirms that the extension allowlist correctly
              permits safe types and blocks dangerous ones.
    """
    assert validate_file_extension("report.txt") is True
    assert validate_file_extension("notes.md") is True
    assert validate_file_extension("data.csv") is True
    assert validate_file_extension("malware.exe") is False
    assert validate_file_extension("backdoor.php") is False
    assert validate_file_extension("script.sh") is False


def test_valid_attachment_saved_and_read():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/notes.py - save_attachment() / read_attachment()
    Fix hint: No fix needed; verifies that a normal attachment can be saved and
              retrieved without errors when the filename is benign.
    """
    save_attachment("memo.txt", "This is a test memo.")
    content = read_attachment("memo.txt")
    assert content == "This is a test memo."


def test_path_traversal_reads_outside_directory(tmp_path):
    """
    Vulnerability type: Path Traversal (Directory Traversal).
    Location: app/notes.py - read_attachment() joins the filename to _NOTES_DIR
              without resolving or validating the resulting absolute path.
    Fix hint: After joining, call os.path.realpath() on the result and assert that
              it starts with os.path.realpath(_NOTES_DIR). Raise ValueError if not.
    """
    # The isolated_database fixture sets attachments_dir = tmp_path / "attachments".
    # We place a sensitive file one level above that directory.
    sensitive_file = tmp_path / "sensitive_config.txt"
    sensitive_file.write_text("database_password=S3cr3tPa$$w0rd")

    # A '../' prefix navigates from attachments/ up to tmp_path where the file lives.
    try:
        content = read_attachment("../sensitive_config.txt")
        # Reaching this line means path traversal succeeded.
        assert content != "database_password=S3cr3tPa$$w0rd", (
            "Path traversal succeeded – read_attachment returned contents of a file "
            "outside the designated attachments directory"
        )
    except (FileNotFoundError, OSError):
        # Expected outcome when path traversal is properly blocked.
        pass
