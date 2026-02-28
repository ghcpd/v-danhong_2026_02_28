"""
run_tests.py – One-click test runner for the SecureVault vulnerability test suite.

Usage:
    python run_tests.py

Runs all tests located under the 'tests/' directory using pytest, prints a
pass/fail summary to the console, and writes the full output to
'logs/test_results.txt' (the directory is created automatically if absent).
"""

import os
import subprocess
import sys


LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
RESULTS_FILE = os.path.join(LOGS_DIR, "test_results.txt")
TESTS_DIR = os.path.join(os.path.dirname(__file__), "tests")


def main() -> None:
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Run pytest with verbose output and no colour codes so the log file is readable.
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            TESTS_DIR,
            "-v",
            "--tb=short",
            "--no-header",
            "--color=no",
        ],
        capture_output=True,
        text=True,
    )

    combined_output = result.stdout
    if result.stderr:
        combined_output += "\nSTDERR:\n" + result.stderr

    # Write the full output to the log file.
    with open(RESULTS_FILE, "w", encoding="utf-8") as fh:
        fh.write(combined_output)

    # Echo the output to the console as-is (pytest already formats the summary).
    print(combined_output, end="")

    print(f"\nFull results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
