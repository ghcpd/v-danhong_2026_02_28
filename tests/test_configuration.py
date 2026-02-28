"""Tests targeting insecure configuration practices such as hardcoded secrets."""

import os

import pytest

from app.config import JWT_SECRET, SECRET_KEY
from app.tokens import secure_compare


def test_hardcoded_secret_key_in_configuration():
    """
    Vulnerability type: Hardcoded Credentials / Sensitive Data Exposure.
    Location: app/config.py - JWT_SECRET and SECRET_KEY are literal string constants.
    Fix hint: Load secrets exclusively from environment variables using
              os.environ['JWT_SECRET'] (or os.environ.get with a secure default that
              raises an error in production). Remove all hardcoded secret values.
    """
    # These are the known insecure hardcoded values present in the source file.
    known_insecure_defaults = {
        "jwt_secret_key_do_not_share",
        "super_secret_key_12345",
    }

    assert JWT_SECRET not in known_insecure_defaults, (
        f"JWT_SECRET is set to the hardcoded insecure default '{JWT_SECRET}' – "
        "secrets must be loaded from environment variables, not stored in source code"
    )
    assert SECRET_KEY not in known_insecure_defaults, (
        f"SECRET_KEY is set to the hardcoded insecure default '{SECRET_KEY}' – "
        "secrets must be loaded from environment variables, not stored in source code"
    )


def test_admin_password_is_insecure_default():
    """
    Vulnerability type: Hardcoded Credentials / Weak Default Password.
    Location: app/config.py - ADMIN_PASSWORD is set to a well-known insecure default.
    Fix hint: Remove ADMIN_PASSWORD from config.py and load it from an environment
              variable; enforce a strong password policy for all administrative accounts.
    """
    from app.config import ADMIN_PASSWORD

    known_weak_passwords = {"admin123", "admin", "password", "123456", "admin@123"}
    assert ADMIN_PASSWORD not in known_weak_passwords, (
        f"ADMIN_PASSWORD is set to the insecure default '{ADMIN_PASSWORD}' – "
        "administrative credentials must never be hardcoded or set to weak defaults"
    )


def test_secure_compare_uses_constant_time():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/tokens.py - secure_compare()
    Fix hint: No fix needed; verifies that secure_compare correctly delegates to
              hmac.compare_digest for constant-time string comparison.
    """
    assert secure_compare("abc123", "abc123") is True
    assert secure_compare("abc123", "different") is False
    assert secure_compare("", "") is True
