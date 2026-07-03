from __future__ import annotations

from typing import Any, Mapping, Sequence


def score_top2_packet(top2_packet: Mapping[str, Any], reference_output: Sequence[Any]) -> dict[str, Any]:
    attempts = top2_packet.get("attempts", []) if isinstance(top2_packet.get("attempts"), list) else []
    matches = [attempt.get("grid") == list(reference_output) for attempt in attempts[:2]]
    return {
        "valid": True,
        "task_score": 1 if any(matches) else 0,
        "solver_exact": bool(matches[0]) if len(matches) > 0 else False,
        "baseline_exact": bool(matches[1]) if len(matches) > 1 else False,
        "malformed_count": 0,
        "error_count": 0,
        "metadata_only": True,
    }
