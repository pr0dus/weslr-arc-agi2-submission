# WESLR ARC-AGI-2 Kaggle Submission JSON Shape Repair V1

## Start HEAD
- `eece476e16a28173ae2ae74200e6360e9762d453`

## End HEAD
- `30820c4e27b86c0d6995b7017016b842cd65a657`

## Files changed
- `src/weslr_arc_solver/emitter.py`
- `src/weslr_arc_solver/solver.py`
- `src/weslr_arc_solver/__init__.py`
- `tests/test_dummy_no_data_smoke.py`
- `README.md`

## Kaggle output shape
### Old WESLR output shape
```json
[{"task_id": "...", "score": 1}]
```

### Repaired WESLR output shape
```json
{
  "TASK_ID": [
    {
      "attempt_1": [[0, 0], [0, 0]],
      "attempt_2": [[0, 0], [0, 0]]
    }
  ]
}
```

## What changed
- Top-level submission is now a dict keyed by `task_id`.
- Each `task_id` maps to a list of prediction objects.
- Each prediction object contains `attempt_1` and `attempt_2`.
- No `score` field is emitted.
- Multiple test inputs are preserved as multiple prediction objects in the list.
- The notebook skeleton still writes `submission.json` locally.

## Tests added / updated
In `tests/test_dummy_no_data_smoke.py`:
- JSON-valid top-level dict check
- task-id key preservation check
- list-per-task check
- `attempt_1` / `attempt_2` presence checks
- nested grid list checks
- no-`score` check
- multiple-test-input shape check
- skeleton-level `submission.json` generation check

## Validation
- `git status --short`: clean after removing the local dry-run artifact and before final packaging steps ✅
- `git diff --check`: pass ✅
- `python -m pytest -q`: pass ✅ (`3 passed`)
- manifest coverage/hash check: pass ✅
- import isolation check: pass ✅
- private path / secret scan: pass ✅
- claim scan: pass ✅

## Kaggle data committed
- No ✅

## Submission made
- No ✅

## Readiness verdict
- `kaggle_sample_submission_format_repaired_ready_for_notebook_preview_test`

## Next recommended lane
- Re-run the Kaggle notebook preview test against the repaired output shape, then compare the generated `submission.json` against Kaggle’s mounted `sample_submission.json` before any Submit Prediction action.
