# SecureVault – Security Vulnerability Challenge

## Project Overview

SecureVault is a deliberately insecure Python application designed as a **security-vulnerability challenge repository**. The codebase implements a minimal user-authentication and note-management library backed by SQLite. It intentionally contains **six distinct, real-world security vulnerabilities** woven naturally into the business logic.

The repository is paired with an automated test suite (pytest) that exercises both secure and insecure code paths. The challenge objective is to **identify and fix every vulnerability** until the full test suite passes.

---

## Installation

**Requirements:** Python 3.12.10 · pip 25.0.1

```bash
# 1. Clone / enter the repository root
cd path/to/securevault

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Tests

```bash
python run_tests.py
```

* Executes all tests under `tests/` via pytest.
* Prints a per-test pass/fail report and a summary to the console.
* Writes the full output to `logs/test_results.txt` (directory is created automatically).

You can also run pytest directly for richer options:

```bash
pytest tests/ -v
```

---

## Embedded Vulnerability Checklist

The following vulnerability categories are present in the source code.  
Specific file locations are intentionally omitted to preserve the challenge.

- [ ] SQL Injection
- [ ] Weak Cryptographic Hash Algorithm (password storage)
- [ ] Timing Attack / Non-Constant-Time Comparison
- [ ] OS Command Injection
- [ ] Insecure Deserialization
- [ ] Path Traversal (Directory Traversal)
- [ ] Hardcoded Secrets / Sensitive Data Exposure in Source Code

---

## Challenge Objective

1. Run `python run_tests.py` to see the **baseline** pass/fail state (roughly 40–50 % of tests pass initially).
2. Read each failing test's docstring – it states the **vulnerability type**, its **location in the codebase**, and a **concise fix hint**.
3. Modify the application source code (files under `app/`) to remediate the vulnerability described by each failing test.
4. Re-run `python run_tests.py` after each fix and confirm progress.
5. The challenge is complete when **all tests pass**.

> **Rule:** Modify only the application source code under `app/`. Do **not** alter test files or `run_tests.py`.

---

## Repository Structure

```
securevault/
├── app/
│   ├── __init__.py
│   ├── auth.py          # User registration & login
│   ├── config.py        # Application configuration
│   ├── database.py      # SQLite connection & schema
│   ├── notes.py         # Note management & file attachments
│   ├── tokens.py        # Token generation & verification
│   └── utils.py         # Utility helpers (serialisation, OS commands)
├── tests/
│   ├── conftest.py
│   ├── test_authentication.py
│   ├── test_configuration.py
│   ├── test_cryptography.py
│   ├── test_deserialization.py
│   ├── test_file_handling.py
│   └── test_injection.py
├── logs/
│   └── test_results.txt   # Baseline output from the first run
├── run_tests.py
├── requirements.txt
└── README.md
```
