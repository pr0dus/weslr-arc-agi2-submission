from __future__ import annotations

from typing import Any, Mapping

_FORBIDDEN_KEYS = {
    "expected_output",
    "reference_output",
    "reference_grid",
    "latent_rule",
    "answer_descriptor",
    "raw_task_json",
}


def redact_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        lowered = payload.lower()
        return "[redacted]" if any(needle in lowered for needle in _FORBIDDEN_KEYS) else payload
    if isinstance(payload, Mapping):
        return {str(k): redact_payload(v) for k, v in payload.items() if str(k).lower() not in _FORBIDDEN_KEYS}
    if isinstance(payload, list):
        return [redact_payload(item) for item in payload]
    if isinstance(payload, tuple):
        return [redact_payload(item) for item in payload]
    return payload
