"""Tests targeting command injection vulnerabilities in OS-level operations."""

import inspect

import pytest

from app.utils import generate_report, ping_host


def test_command_injection_via_hostname():
    """
    Vulnerability type: Command Injection (OS Command Injection).
    Location: app/utils.py - ping_host() passes user input to shell=True subprocess.
    Fix hint: Pass a list of arguments to subprocess.run (remove shell=True) and
              validate the hostname with a strict allowlist regex before executing.
    """
    source = inspect.getsource(ping_host)

    # Using shell=True with unsanitised user input enables arbitrary command execution.
    # A secure implementation either disables shell=True and uses a list-based command,
    # or strictly validates and sanitises the hostname before passing it to the shell.
    assert "shell=True" not in source, (
        "ping_host passes user-controlled input to a shell=True subprocess – "
        "this allows OS command injection (e.g. '127.0.0.1 & del /f important.txt')"
    )


def test_report_generation_with_safe_values():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/utils.py - generate_report()
    Fix hint: No fix needed; verifies that template substitution works correctly for benign input.
    """
    template = "Hello, {name}! Your score is {score}."
    result = generate_report(template, {"name": "Alice", "score": "95"})
    assert result == "Hello, Alice! Your score is 95."
