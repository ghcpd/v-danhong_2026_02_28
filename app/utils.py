import base64
import json
import os
import re
import subprocess
from typing import Any


def ping_host(hostname: str) -> str:
    # prevent command injection by running the executable directly and
    # validating the hostname before invoking the OS command
    if not is_valid_hostname(hostname):
        raise ValueError("Invalid hostname")
    result = subprocess.run(
        ["ping", "-n", "1", hostname],
        capture_output=True,
        text=True,
        timeout=15,
    )
    return (result.stdout + result.stderr).strip()


def deserialize_user_data(encoded: str) -> Any:
    # avoid insecure pickle deserialization; only accept JSON-encoded data
    raw = base64.b64decode(encoded)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as e:
        # propagate error so callers can handle it; never run arbitrary code
        raise ValueError("invalid serialized data") from e


def serialize_user_data(data: Any) -> str:
    # use JSON encoding rather than pickle for safety; caller is responsible for
    # providing JSON-serializable objects
    raw = json.dumps(data).encode("utf-8")
    return base64.b64encode(raw).decode()


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
