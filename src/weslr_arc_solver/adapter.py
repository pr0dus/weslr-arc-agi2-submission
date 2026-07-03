from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from .grid import copy_grid
from .public_gate import FIXTURE_PATH, build_dummy_approval_manifest, validate_dummy_approval_manifest
from .schema import ALLOWED_PACKET_KEYS, DUMMY_SOURCE_KIND, SCHEMA_VERSION


_REPO_ROOT = Path(__file__).resolve().parents[2]
_FIXTURE_ABS = _REPO_ROOT / FIXTURE_PATH


def _checksum() -> str:
    return hashlib.sha256(_FIXTURE_ABS.read_bytes()).hexdigest()


def load_dummy_fixture_text() -> str:
    return _FIXTURE_ABS.read_text(encoding="utf-8")


def _validate_structure(data: Mapping[str, Any]) -> None:
    if data.get("dummy_no_data") is not True:
        raise ValueError("dummy fixture marker missing")
    if data.get("source_kind") != DUMMY_SOURCE_KIND:
        raise ValueError("dummy source kind mismatch")


def build_dummy_bundle(manifest: Any | None = None) -> dict[str, Any]:
    approval = build_dummy_approval_manifest() if manifest is None else manifest
    validated = validate_dummy_approval_manifest(approval)
    payload = json.loads(load_dummy_fixture_text())
    _validate_structure(payload)
    solver_visible_tasks = []
    scorer_reference_tasks = []
    for idx, task in enumerate(payload.get("tasks", [])):
        solver_visible_tasks.append(
            {
                "task_id": f"anon_dummy_{idx:03d}",
                "anonymized_task_id": f"anon_dummy_{idx:03d}",
                "train_pairs": [
                    {"input_grid": deepcopy(pair["input_grid"]), "output_grid": deepcopy(pair["output_grid"])}
                    for pair in task.get("train_pairs", [])
                ],
                "test_inputs": [
                    {"test_input_index": test_idx, "input_grid": deepcopy(test["input_grid"])}
                    for test_idx, test in enumerate(task.get("test_inputs", []))
                ],
                "required_output_count": 2,
                "format_metadata": {"format_id": "arc_grid_v1", "json_safe": True},
                "parse_status": "parsed",
                "source_kind": DUMMY_SOURCE_KIND,
                "packet_metadata": {"dummy_no_data": True, "solver_visible": True},
            }
        )
        scorer_reference_tasks.append(
            {
                "task_id": f"anon_dummy_{idx:03d}",
                "reference_output": deepcopy(task.get("reference_outputs", [{}])[0].get("output_grid", [])),
                "packet_metadata": {"dummy_no_data": True, "scorer_visible": True},
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "dummy_no_data": True,
        "official_data_touched": False,
        "public_data_touched": False,
        "network_touched": False,
        "source_checksum": _checksum(),
        "approval_manifest": validated,
        "solver_visible_tasks": solver_visible_tasks,
        "scorer_reference_tasks": scorer_reference_tasks,
        "anonymized_task_ids": [item["anonymized_task_id"] for item in solver_visible_tasks],
    }


def validate_solver_visible_packet(packet: Any) -> dict[str, Any]:
    if not isinstance(packet, Mapping):
        raise ValueError("solver-visible packet must be a mapping")
    if not set(ALLOWED_PACKET_KEYS).issubset(set(packet.keys())):
        raise ValueError("solver-visible packet missing required keys")
    if packet.get("required_output_count") != 2:
        raise ValueError("solver-visible packet must require exactly two outputs")
    text = json.dumps(packet, ensure_ascii=False).lower()
    for needle in ("expected_output", "reference_output", "latent_rule", "answer_descriptor"):
        if needle in text:
            raise ValueError(f"forbidden field leaked: {needle}")
    return {"valid": True, "anonymized_task_id": str(packet.get("anonymized_task_id"))}


load_dummy_bundle = build_dummy_bundle


__all__ = ["build_dummy_bundle", "build_dummy_approval_manifest", "load_dummy_bundle", "load_dummy_fixture_text", "validate_solver_visible_packet"]
