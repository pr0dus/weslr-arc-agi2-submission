from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .grid import copy_grid, invert_binary_grid, validate_grid


def infer_rule(train_pairs: list[Mapping[str, Any]]) -> str:
    copy_fit = True
    invert_fit = True
    for pair in train_pairs:
        if pair.get("input_grid") != pair.get("output_grid"):
            copy_fit = False
        if invert_binary_grid(pair.get("input_grid", [])) != pair.get("output_grid"):
            invert_fit = False
    if copy_fit:
        return "copy_input"
    if invert_fit:
        return "invert_binary"
    return "copy_input"


def emit_two_outputs(solver_visible_packet: Mapping[str, Any]) -> dict[str, Any]:
    test_inputs = solver_visible_packet.get("test_inputs", [])
    if not test_inputs:
        raise ValueError("test inputs required")
    test_grid = deepcopy(test_inputs[0].get("input_grid", []))
    validate_grid(test_grid)
    rule = infer_rule(list(solver_visible_packet.get("train_pairs", [])))
    predicted = copy_grid(test_grid) if rule == "copy_input" else invert_binary_grid(test_grid)
    baseline = invert_binary_grid(test_grid) if rule == "copy_input" else copy_grid(test_grid)
    validate_grid(predicted)
    validate_grid(baseline)
    return {
        "rule": rule,
        "candidate_grids": [predicted, baseline],
        "top2_packet": {
            "task_id": solver_visible_packet.get("task_id"),
            "attempts": [
                {"rank": 1, "grid": predicted, "confidence_label": "high"},
                {"rank": 2, "grid": baseline, "confidence_label": "low"},
            ],
            "metadata": {"exact_two_output_required": True, "dummy_no_data": True},
        },
    }
