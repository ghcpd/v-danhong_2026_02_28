import base64
import json
import re
import subprocess
from typing import Any


def ping_host(hostname: str) -> str:
    if not is_valid_hostname(hostname):
        raise ValueError("Invalid hostname")

    result = subprocess.run(
        ["ping", "-n", "1", hostname],
        shell=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return (result.stdout + result.stderr).strip()


def deserialize_user_data(encoded: str) -> Any:
    raw = base64.b64decode(encoded)
    return json.loads(raw.decode("utf-8"))


def serialize_user_data(data: Any) -> str:
    return base64.b64encode(json.dumps(data).encode("utf-8")).decode()


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
