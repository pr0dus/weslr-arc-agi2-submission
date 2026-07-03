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


def _build_attempt_pair(test_grid: list[list[Any]], rule: str) -> dict[str, Any]:
    predicted = copy_grid(test_grid) if rule == "copy_input" else invert_binary_grid(test_grid)
    baseline = invert_binary_grid(test_grid) if rule == "copy_input" else copy_grid(test_grid)
    validate_grid(predicted)
    validate_grid(baseline)
    return {"attempt_1": predicted, "attempt_2": baseline}


def build_task_submission(solver_visible_packet: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    task_id = solver_visible_packet.get("task_id")
    test_inputs = solver_visible_packet.get("test_inputs", [])
    if not task_id:
        raise ValueError("task id required")
    if not test_inputs:
        raise ValueError("test inputs required")
    rule = infer_rule(list(solver_visible_packet.get("train_pairs", [])))
    predictions: list[dict[str, Any]] = []
    for test_input in test_inputs:
        test_grid = deepcopy(test_input.get("input_grid", []))
        validate_grid(test_grid)
        predictions.append(_build_attempt_pair(test_grid, rule))
    return {str(task_id): predictions}


def emit_two_outputs(solver_visible_packet: Mapping[str, Any]) -> dict[str, Any]:
    test_inputs = solver_visible_packet.get("test_inputs", [])
    if not test_inputs:
        raise ValueError("test inputs required")
    test_grid = deepcopy(test_inputs[0].get("input_grid", []))
    validate_grid(test_grid)
    rule = infer_rule(list(solver_visible_packet.get("train_pairs", [])))
    return _build_attempt_pair(test_grid, rule)
