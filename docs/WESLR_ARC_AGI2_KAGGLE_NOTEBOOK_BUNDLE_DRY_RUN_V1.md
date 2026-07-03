# WESLR ARC-AGI-2 Kaggle Notebook Bundle Dry Run V1

## Current public repo HEAD
- `d2fe40ff4ea0db679c350edc034c3f72231be126`

## Dry-run bundle directory
- `/data/data/com.termux/files/home/.openclaw/workspace/tmp/weslr-arc-agi2-kaggle-bundle`

## Expected Kaggle notebook layout
Recommended notebook workspace layout:
```
submission_notebook_skeleton.py
src/
  weslr_arc_solver/
    __init__.py
    adapter.py
    emitter.py
    grid.py
    public_gate.py
    redaction.py
    schema.py
    scorer.py
    solver.py
```

## How the notebook imports the package
- The skeleton bootstraps a local `src/` directory onto `sys.path`.
- It prefers `Path(__file__).resolve().parent / "src"` when the file is present.
- It falls back to `Path.cwd() / "src"`.
- Import target: `from weslr_arc_solver.solver import run_submission_skeleton`

## Expected input path assumptions
- The current dry-run bundle does not require competition input files.
- The notebook path logic is local-only and no-internet.
- For a real Kaggle competition notebook, the owner must verify the actual Kaggle-provided input location inside the notebook environment before final submission.
- The notebook must not depend on Android/Termux paths, GitHub fetches, or private WESLR paths.

## Expected output path
- The skeleton writes `submission.json` in the current notebook working directory.
- The output should be JSON-valid and created locally before any real submission.

## Files included in the dry-run bundle
Runtime-only bundle contents:
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
- `tests/fixtures/dummy_no_data/arc_official_public_dummy_no_data_v1.json`

## Files excluded from the dry-run bundle
Do not include:
- `.git/`
- `.pytest_cache/`
- `__pycache__/`
- `tests/` except the one runtime fixture file listed above
- `docs/`
- `README.md`
- `MANIFEST.sha256`
- `EXPORT_AUDIT.md`
- `EXPORT_REPORT.md`
- `LICENSE`
- `NOTICE.md`
- private WESLR files, private paths, or sensitive values
- official/public ARC data files not already in the public repo
- any Android/Termux-only paths

## How the owner should upload/attach it in Kaggle
1. Open the competition notebook workspace.
2. Upload or attach the public bundle contents.
3. Place `submission_notebook_skeleton.py` and the `src/` tree in the notebook workspace.
4. Confirm the notebook can resolve `weslr_arc_solver` locally.
5. Run a dry execution before any final submission.

## Exact manual steps before pressing Submit Prediction
1. Open the notebook preview.
2. Verify imports resolve without internet.
3. Run the notebook once and confirm `submission.json` is written.
4. Inspect the output file contents and shape.
5. Confirm no private paths, secrets, or unsupported claims are present.
6. Confirm the notebook does not depend on GitHub or Android paths.
7. Only then press **Submit Prediction** manually.

## Stop conditions before any real submission
Stop if any of these are true:
- the notebook cannot import the bundled source
- the notebook needs network access
- the notebook needs GitHub access
- the notebook needs private WESLR/OCC/OpenClaw/Nova/.weslr paths
- the notebook cannot produce a valid local `submission.json`
- any official/public ARC data would need to be copied into the repo or bundle
- any unsupported claim wording appears in repo docs or notebook text

## Local dry-run commands
From the public checkout or the bundle directory:
```bash
PYTHONPATH=src python -c "import weslr_arc_solver; print('import OK')"
python submission_notebook_skeleton.py
python - <<'PY'
from pathlib import Path
import json
p = Path('submission.json')
print('exists', p.exists())
print('json_valid', isinstance(json.loads(p.read_text(encoding='utf-8')), list))
PY
```

## Dry-run outcome expected
- bundled import works
- local `submission.json` is created
- `submission.json` is JSON-valid
- the output shape is the local list-of-results shape produced by the skeleton
- the dummy/no-data path remains separate from real Kaggle execution wiring

## Next recommended lane
- Prepare a Kaggle notebook preview test using the same bundle layout, then inspect the generated `submission.json` before any real submission.
