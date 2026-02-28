"""Tests targeting insecure deserialization vulnerabilities."""

import base64
import os
import pickle

import pytest

from app.utils import deserialize_user_data, safe_json_deserialize, safe_json_serialize


def test_json_serialization_roundtrip():
    """
    Vulnerability type: N/A (positive-path test).
    Location: app/utils.py - safe_json_serialize() / safe_json_deserialize()
    Fix hint: No fix needed; confirms that the JSON-based helpers correctly
              round-trip arbitrary dictionaries.
    """
    original = {"user_id": 7, "role": "editor", "tags": ["python", "security"]}
    encoded = safe_json_serialize(original)
    recovered = safe_json_deserialize(encoded)
    assert recovered == original


def test_pickle_deserialization_arbitrary_code_execution(tmp_path):
    """
    Vulnerability type: Insecure Deserialization (Arbitrary Code Execution via pickle).
    Location: app/utils.py - deserialize_user_data() calls pickle.loads on untrusted data.
    Fix hint: Replace pickle with JSON (json.loads / json.dumps). If binary serialisation
              is required, use a safe alternative such as msgpack with strict schema
              validation; never call pickle.loads on data from an untrusted source.
    """
    # The exploit payload uses __reduce__ to call the built-in open() with a path
    # to a sentinel file.  open() is a picklable callable; the path string is also
    # picklable.  If pickle.loads executes the payload, the sentinel file is created.
    flag_file = str(tmp_path / "exploit_executed.flag")

    class _Exploit:
        def __reduce__(self):
            # pickle.loads will call: open(flag_file, 'w')
            return (open, (flag_file, "w"))

    malicious_payload = base64.b64encode(pickle.dumps(_Exploit())).decode()

    # Ensure the sentinel does not already exist.
    if os.path.exists(flag_file):
        os.remove(flag_file)

    try:
        result = deserialize_user_data(malicious_payload)
        # Close the returned file handle to avoid resource-leak warnings.
        if hasattr(result, "close"):
            result.close()
    except Exception:
        pass  # Even if an error occurs, the file may already have been created.

    # If pickle.loads executed the payload, the file now exists.
    assert not os.path.exists(flag_file), (
        "deserialize_user_data executed arbitrary code from the pickle payload – "
        "calling open() via __reduce__ created a file on disk; "
        "pickle.loads must not be used with untrusted input"
    )
