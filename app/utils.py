import base64
import json
import os
import pickle
import re
import subprocess
from typing import Any


def ping_host(hostname: str) -> str:
    result = subprocess.run(
        f"ping -n 1 {hostname}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return (result.stdout + result.stderr).strip()


def deserialize_user_data(encoded: str) -> Any:
    raw = base64.b64decode(encoded)
    return pickle.loads(raw)


def serialize_user_data(data: Any) -> str:
    return base64.b64encode(pickle.dumps(data)).decode()


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
