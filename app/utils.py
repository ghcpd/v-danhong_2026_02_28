import base64
import json
import os
import re
import subprocess
from typing import Any


def ping_host(hostname: str) -> str:
    # Validate hostname with strict regex to prevent command injection
    if not is_valid_hostname(hostname):
        raise ValueError(f"Invalid hostname: {hostname}")
    # Use list-based command with shell=False to prevent shell injection
    result = subprocess.run(
        ["ping", "-n", "1", hostname],
        capture_output=True,
        text=True,
        timeout=15,
    )
    return (result.stdout + result.stderr).strip()


def deserialize_user_data(encoded: str) -> Any:
    raw = base64.b64decode(encoded)
    # Use json.loads instead of pickle.loads to prevent arbitrary code execution
    return json.loads(raw.decode())


def serialize_user_data(data: Any) -> str:
    # Use json.dumps instead of pickle.dumps for safe serialization
    return base64.b64encode(json.dumps(data).encode()).decode()


def safe_json_serialize(data: dict) -> str:
    return json.dumps(data)


def safe_json_deserialize(payload: str) -> Any:
    return json.loads(payload)


def generate_report(template: str, values: dict) -> str:
    for key, val in values.items():
        template = template.replace(f"{{{key}}}", str(val))
    return template


def is_valid_hostname(hostname: str) -> bool:
    pattern = re.compile(r"^[a-zA-Z0-9.\-]{1,253}$")
    return bool(pattern.match(hostname))
