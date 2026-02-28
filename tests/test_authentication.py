"""Tests targeting authentication-related security vulnerabilities."""

import pytest

from app.auth import login_user, register_user


def test_valid_user_registration():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/auth.py - register_user()
    Fix hint: No fix needed; verifies that normal registration succeeds.
    """
    result = register_user("alice", "StrongPass!99", "alice@example.com")
    assert result["success"] is True
    assert isinstance(result["user_id"], int)


def test_valid_login_with_correct_password():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/auth.py - login_user()
    Fix hint: No fix needed; verifies that a registered user can log in with correct credentials.
    """
    register_user("bob", "C0rrectH0rse!", "bob@example.com")
    result = login_user("bob", "C0rrectH0rse!")
    assert result["success"] is True
    assert result["username"] == "bob"


def test_sql_injection_bypass_authentication():
    """
    Vulnerability type: SQL Injection.
    Location: app/auth.py - login_user() builds the query with f-string formatting.
    Fix hint: Replace the f-string query with a parameterized query using '?' placeholders.
    """
    # Seed a legitimate user so the injected query returns a real row.
    register_user("carol", "SecretPass#1", "carol@example.com")

    # Classic OR-based SQL injection to bypass the password check.
    injected_username = "' OR '1'='1' --"
    result = login_user(injected_username, "wrong_password")

    # A properly hardened implementation must reject this attempt.
    assert result["success"] is False, (
        "SQL injection bypassed authentication – login_user is vulnerable to SQL injection"
    )
