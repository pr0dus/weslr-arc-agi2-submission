# WESLR ARC-AGI-2 Solver Behavior Preservation Review V1

## Start HEAD
- `31be7ae8815f9ab72debd4877d6e943a76330d90`

## Compared pre-repair HEAD
- `eece476e16a28173ae2ae74200e6360e9762d453`

## Current HEAD
- `31be7ae8815f9ab72debd4877d6e943a76330d90`

## Files inspected
- `src/weslr_arc_solver/solver.py`
- `src/weslr_arc_solver/emitter.py`
- `src/weslr_arc_solver/__init__.py`
- `tests/test_dummy_no_data_smoke.py`
- `submission_notebook_skeleton.py`

## What changed in `solver.py`
- The solver loop stopped scoring against reference outputs and now writes Kaggle-shaped predictions.
- The algorithm used to build predictions was not changed.
- Task iteration order was not changed.
- Task IDs were not changed.
- Test-output counts were not changed.
- The change is output-contract-only.

## Old output shape
```json
[
  {"task_id": "anon_dummy_000", "score": 1},
  {"task_id": "anon_dummy_001", "score": 1}
]
```

## New output shape
```json
{
  "anon_dummy_000": [
    {"attempt_1": [[1, 1, 0], [0, 0, 1]], "attempt_2": [[0, 0, 1], [1, 1, 0]]}
  ],
  "anon_dummy_001": [
    {"attempt_1": [[1, 1, 0], [0, 0, 1]], "attempt_2": [[0, 0, 1], [1, 1, 0]]}
  ]
}
```

## Normalized comparison result
- Old output normalized to the new Kaggle shape matched the current output exactly on the dummy/no-data fixture.
- The same task IDs were present.
- The same test-input count was present.
- The same predicted grids were emitted for each task.

## Did predicted grids change?
- No.

## Did task IDs change?
- No.

## Did test-output counts change?
- No.

## Risk introduced by attempt duplication/fallback
- Low.
- The current output keeps two attempts per prediction object as required by the Kaggle sample shape.
- The fallback behavior remains the same safe dummy baseline pairing used before; only the wrapper shape changed.

## Kaggle data committed
- No.

## Submission made
- No.

## Validation
- `git status --short`: clean after report preparation ✅
- `git diff --check`: pass ✅
- `python -m pytest -q`: pass ✅
- manifest coverage/hash check: pass ✅
- import isolation check: pass ✅
- private path / secret scan: pass ✅
- claim scan: pass ✅
- repo remains public: yes ✅

## Verdict
- `solver_behavior_preserved_format_only_change`

## Next recommended lane
- Rerun the Kaggle notebook preview test against the repaired output shape and verify it against Kaggle’s mounted `sample_submission.json` before any submission action.
