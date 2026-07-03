# WESLR ARC-AGI-2 Kaggle Repaired Notebook Preview V1

## Start HEAD
- `d5658f8d973040d9568c3c3d8ffe89546df7c2`

## Bundle path
- Directory: `/data/data/com.termux/files/home/.openclaw/workspace/tmp/weslr-arc-agi2-kaggle-repaired-bundle`
- Zip: `/data/data/com.termux/files/home/.openclaw/workspace/tmp/weslr-arc-agi2-kaggle-repaired-bundle.zip`

## Files included in the bundle
- `submission_notebook_skeleton.py`
- `src/weslr_arc_solver/__init__.py`
- `src/weslr_arc_solver/adapter.py`
- `src/weslr_arc_solver/emitter.py`
- `src/weslr_arc_solver/grid.py`
- `src/weslr_arc_solver/public_gate.py`
- `src/weslr_arc_solver/redaction.py`
- `src/weslr_arc_solver/schema.py`
- `src/weslr_arc_solver/scorer.py`
- `src/weslr_arc_solver/solver.py`

## Files excluded from the bundle
- `.git/`
- `docs/`
- `tests/`
- Kaggle `sample_submission.json`
- Kaggle challenge / solution JSON files
- private WESLR files
- secrets / tokens
- any provider/model/API/web-call code
- any Android/Termux-only paths

## Owner upload / attach instructions
1. Open the Kaggle ARC-AGI-2 notebook workspace.
2. Upload or attach the bundle contents.
3. Ensure the notebook workspace contains:
   - `submission_notebook_skeleton.py`
   - `src/weslr_arc_solver/`
4. Keep internet disabled.
5. Run the preview cell below before any Submit Prediction action.

## Kaggle notebook preview cell
```python
from pathlib import Path
import json
import sys

SRC = Path("/kaggle/input/<your-upload-bundle>/src")
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from weslr_arc_solver.emitter import build_task_submission

INPUT_ROOT = Path("/kaggle/input/competitions/arc-prize-2026-arc-agi-2")
WORKING = Path("/kaggle/working")

with (INPUT_ROOT / "arc-agi_test_challenges.json").open("r", encoding="utf-8") as f:
    challenges = json.load(f)

submission = {}
for task_id, task in challenges.items():
    solver_visible_packet = {
        "task_id": task_id,
        "train_pairs": [
            {"input_grid": pair["input"], "output_grid": pair["output"]}
            for pair in task["train"]
        ],
        "test_inputs": [
            {"test_input_index": i, "input_grid": test_item["input"]}
            for i, test_item in enumerate(task["test"])
        ],
    }
    submission.update(build_task_submission(solver_visible_packet))

(WORKING / "submission.json").write_text(json.dumps(submission, indent=2), encoding="utf-8")

with (INPUT_ROOT / "sample_submission.json").open("r", encoding="utf-8") as f:
    sample = json.load(f)

ok = True
ok &= isinstance(submission, dict)
ok &= isinstance(sample, dict)
ok &= len(submission) == len(sample)
ok &= set(submission) == set(sample)
ok &= all(isinstance(v, list) for v in submission.values())
ok &= all(set(item.keys()) == {"attempt_1", "attempt_2"} for v in submission.values() for item in v)
ok &= all("score" not in item for v in submission.values() for item in v)

print("PASS" if ok else "FAIL")
```

## Preview cell behavior
- adds bundled `src` to `sys.path`
- imports `weslr_arc_solver`
- reads Kaggle `arc-agi_test_challenges.json`
- writes `/kaggle/working/submission.json`
- loads Kaggle `sample_submission.json`
- checks top-level type
- checks task-id coverage and value list type
- checks `attempt_1` / `attempt_2`
- checks that no `score` field is emitted

## Validation performed locally
- Repaired bundle dry-run against synthetic Kaggle-shaped files: PASS
- `submission.json` written locally by the preview logic: PASS
- top-level dict / task-id key / list-per-task / attempt fields / no-score checks: PASS

## No Kaggle data committed
- No.

## No submission made
- No.

## Readiness verdict
- `repaired_kaggle_notebook_bundle_ready_for_owner_preview_run`

## Next recommended lane
- Run the preview cell inside the Kaggle notebook and confirm its PASS output against the mounted sample submission before any submit action.
