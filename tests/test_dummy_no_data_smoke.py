from __future__ import annotations

import json

from weslr_arc_solver.adapter import build_dummy_bundle
from weslr_arc_solver.emitter import build_task_submission, emit_two_outputs
from weslr_arc_solver.redaction import redact_payload
from weslr_arc_solver.solver import run_submission_skeleton


def test_dummy_no_data_smoke() -> None:
    bundle = build_dummy_bundle()
    assert bundle["official_data_touched"] is False
    assert bundle["public_data_touched"] is False
    assert bundle["network_touched"] is False
    assert bundle["approval_manifest"]["dummy_no_data"] is True
    assert len(bundle["solver_visible_tasks"]) == 2
    assert bundle["anonymized_task_ids"] == ["anon_dummy_000", "anon_dummy_001"]

    task = bundle["solver_visible_tasks"][0]
    emission = emit_two_outputs(task)
    assert set(emission.keys()) == {"attempt_1", "attempt_2"}
    assert len(emission["attempt_1"]) == len(emission["attempt_2"])

    submission = build_task_submission(task)
    assert list(submission.keys()) == [task["task_id"]]
    assert isinstance(submission[task["task_id"]], list)
    assert len(submission[task["task_id"]]) == len(task["test_inputs"])
    first_prediction = submission[task["task_id"]][0]
    assert set(first_prediction.keys()) == {"attempt_1", "attempt_2"}
    assert isinstance(first_prediction["attempt_1"], list)
    assert isinstance(first_prediction["attempt_2"], list)
    assert "score" not in json.dumps(submission)

    # Preserve the exact-two-attempt fallback behavior for dummy smoke coverage.
    assert emission["attempt_1"] == first_prediction["attempt_1"]
    assert emission["attempt_2"] == first_prediction["attempt_2"]

    redacted = redact_payload({"expected_output": [[1]], "source_checksum": "abc"})
    assert json.dumps(redacted) == '{"source_checksum": "abc"}'


def test_submission_shape_handles_multiple_test_inputs() -> None:
    bundle = build_dummy_bundle()
    task = dict(bundle["solver_visible_tasks"][0])
    task["task_id"] = "anon_dummy_multi"
    task["test_inputs"] = [
        {"test_input_index": 0, "input_grid": [[1, 1], [0, 0]]},
        {"test_input_index": 1, "input_grid": [[0, 1], [1, 0]]},
    ]

    submission = build_task_submission(task)
    assert list(submission.keys()) == ["anon_dummy_multi"]
    predictions = submission["anon_dummy_multi"]
    assert len(predictions) == 2
    for prediction in predictions:
        assert set(prediction.keys()) == {"attempt_1", "attempt_2"}
        assert isinstance(prediction["attempt_1"], list)
        assert isinstance(prediction["attempt_2"], list)
        assert "score" not in prediction


def test_submission_skeleton_writes_kaggle_shape(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    run_submission_skeleton()

    submission_path = tmp_path / "submission.json"
    assert submission_path.exists()
    data = json.loads(submission_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert set(data.keys()) == {"anon_dummy_000", "anon_dummy_001"}
    for task_id, predictions in data.items():
        assert isinstance(predictions, list)
        assert predictions
        for prediction in predictions:
            assert set(prediction.keys()) == {"attempt_1", "attempt_2"}
            assert isinstance(prediction["attempt_1"], list)
            assert isinstance(prediction["attempt_2"], list)
            assert "score" not in prediction
