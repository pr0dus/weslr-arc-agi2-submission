from __future__ import annotations

import json
from pathlib import Path

from .adapter import build_dummy_bundle
from .emitter import build_task_submission


def run_submission_skeleton() -> None:
    bundle = build_dummy_bundle()
    outputs: dict[str, list[dict[str, object]]] = {}
    for task in bundle["solver_visible_tasks"]:
        outputs.update(build_task_submission(task))
    Path("submission.json").write_text(json.dumps(outputs, indent=2), encoding="utf-8")
