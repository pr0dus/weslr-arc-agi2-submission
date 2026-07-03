from __future__ import annotations

import json
from pathlib import Path

from .adapter import build_dummy_bundle
from .emitter import emit_two_outputs
from .scorer import score_top2_packet


def run_submission_skeleton() -> None:
    bundle = build_dummy_bundle()
    outputs = []
    for task, reference in zip(bundle["solver_visible_tasks"], bundle["scorer_reference_tasks"]):
        emission = emit_two_outputs(task)
        score = score_top2_packet(emission["top2_packet"], reference["reference_output"])
        outputs.append({"task_id": task["task_id"], "score": score["task_score"]})
    Path("submission.json").write_text(json.dumps(outputs, indent=2), encoding="utf-8")
