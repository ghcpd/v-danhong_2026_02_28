"""Tests targeting cryptographic weaknesses in password hashing and token verification."""

import hashlib
import inspect

import pytest

from app.auth import hash_password, verify_password
from app.tokens import verify_token


def test_password_verification_works():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/auth.py - verify_password()
    Fix hint: No fix needed; confirms that verify_password correctly validates passwords.
    """
    hashed = hash_password("MyP@ssw0rd!")
    assert verify_password("MyP@ssw0rd!", hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_password_hash_is_cryptographically_weak():
    """
    Vulnerability type: Weak Cryptographic Hash (MD5).
    Location: app/auth.py - hash_password() uses hashlib.md5.
    Fix hint: Replace hashlib.md5 with bcrypt, argon2-cffi, or at minimum
              hashlib.pbkdf2_hmac('sha256', ...) with a random salt.
    """
    pw_hash = hash_password("anypassword")

    # MD5 always produces a 32-character hex digest.
    # A strong password-hashing scheme (bcrypt, argon2) yields at least 60 characters
    # and embeds the salt within the encoded output.
    assert len(pw_hash) >= 60, (
        f"Password hash is only {len(pw_hash)} characters long – "
        "this indicates a weak algorithm (MD5 produces 32 hex chars)"
    )


def test_timing_attack_in_token_verification():
    """
    Vulnerability type: Timing Attack / Non-Constant-Time Comparison.
    Location: app/tokens.py - verify_token() compares signatures with '==' operator.
    Fix hint: Replace the '==' comparison with hmac.compare_digest() to ensure
              constant-time string comparison and prevent timing-based side-channel attacks.
    """
    source = inspect.getsource(verify_token)

    # A secure implementation must use hmac.compare_digest for signature comparison.
    assert "compare_digest" in source, (
        "verify_token uses '==' for signature comparison – "
        "this is vulnerable to timing attacks; use hmac.compare_digest instead"
    )
