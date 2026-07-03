from __future__ import annotations

import json

from weslr_arc_solver.adapter import build_dummy_bundle
from weslr_arc_solver.emitter import emit_two_outputs
from weslr_arc_solver.redaction import redact_payload
from weslr_arc_solver.scorer import score_top2_packet


def test_dummy_no_data_smoke() -> None:
    bundle = build_dummy_bundle()
    assert bundle["official_data_touched"] is False
    assert bundle["public_data_touched"] is False
    assert bundle["network_touched"] is False
    assert bundle["approval_manifest"]["dummy_no_data"] is True
    assert len(bundle["solver_visible_tasks"]) == 2
    assert bundle["anonymized_task_ids"] == ["anon_dummy_000", "anon_dummy_001"]

    task = bundle["solver_visible_tasks"][0]
    reference = bundle["scorer_reference_tasks"][0]["reference_output"]
    emission = emit_two_outputs(task)
    assert len(emission["candidate_grids"]) == 2
    assert emission["top2_packet"]["metadata"]["exact_two_output_required"] is True

    score = score_top2_packet(emission["top2_packet"], reference)
    assert score["task_score"] == 1
    assert score["solver_exact"] is True
    assert score["baseline_exact"] is False

    redacted = redact_payload({"expected_output": [[1]], "source_checksum": "abc"})
    assert json.dumps(redacted) == '{"source_checksum": "abc"}'
