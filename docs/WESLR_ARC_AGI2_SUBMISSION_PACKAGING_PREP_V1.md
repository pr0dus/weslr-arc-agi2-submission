# WESLR ARC-AGI-2 Submission Packaging Prep V1

## Current public repo HEAD
- Prep reference HEAD at the start of this checklist: `8b7f484e68730adf2ddacd11ec8c24429aeed91c`

## Official requirements checked
Official sources reviewed:
- ARC Prize ARC-AGI-2 page: https://arcprize.org/arc-agi/2
- ARC Prize Research page: https://arcprize.org/research

Observed packaging-relevant points from the official ARC pages:
- ARC-AGI-2 is a calibrated benchmark with public, semi-private, and private eval sets.
- The benchmark expects efficient reasoning systems and pass@2-style task handling.
- Public training/eval data is separate from hidden contest data.
- No official/public ARC dataset files were copied into this repo for prep.

Kaggle-side docs probes were attempted at:
- https://www.kaggle.com/docs/notebooks
- https://www.kaggle.com/docs/competitions
- https://www.kaggle.com/docs/submissions

Those Kaggle docs requests were blocked by reCAPTCHA in this environment, so no usable text was captured here. Packaging assumptions below therefore stay conservative and align with the repo's no-internet design plus the official ARC pages above.

## Expected notebook / file layout
- Notebook entrypoint: `submission_notebook_skeleton.py`
- Bundled local package: `src/weslr_arc_solver/`
- Notebook execution must resolve imports from bundled source only.
- The notebook skeleton now bootstraps `src/` onto `sys.path` before importing the solver.
- Runtime output file written by the skeleton: `submission.json` in the current working directory.

## Expected input / output path assumptions
- Input should come from Kaggle-provided local files only.
- No network, API, provider, or model calls.
- The run should not rely on manual repair after execution starts.
- The solver should emit exactly two outputs per test input when required.
- The current skeleton writes a JSON submission artifact locally rather than depending on external services.

## Exact files needed for a submission bundle
Minimum execution bundle:
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

Repository prep / local validation files that can remain in the public repo but are not required in an actual Kaggle execution bundle:
- `README.md`
- `requirements.txt`
- `tests/test_dummy_no_data_smoke.py`
- `tests/conftest.py`
- `docs/METHOD.md`
- `docs/REPRODUCIBILITY.md`
- `docs/NO_INTERNET_EVALUATION.md`
- `docs/PRIVATE_EXCLUSION_CHECKLIST.md`
- `MANIFEST.sha256`
- `LICENSE`
- `NOTICE.md`
- `EXPORT_AUDIT.md`
- `EXPORT_REPORT.md`
- `.gitignore`

## Exact files not to include
Do not include any of the following in a real submission bundle:
- `.git/`
- `.pytest_cache/`
- `__pycache__/`
- `tests/`
- `docs/`
- `README.md`
- `MANIFEST.sha256`
- `EXPORT_AUDIT.md`
- `EXPORT_REPORT.md`
- `LICENSE`
- `NOTICE.md`
- any `*.pyc` files
- any private WESLR files, private paths, or sensitive values
- any official/public ARC data files not already present in the public repo

## Commands to validate locally
```bash
python -m pytest -q tests/test_dummy_no_data_smoke.py
PYTHONPATH=src python -c "import weslr_arc_solver; print('weslr_arc_solver import OK')"
python submission_notebook_skeleton.py
python - <<'PY'
from pathlib import Path
print(Path('submission.json').exists())
PY
```

## Stop conditions before real submission
Stop if any of these are true:
- the notebook cannot import bundled source locally
- the notebook needs internet, API, provider, or model access
- the notebook depends on private WESLR context or manual repair
- an unsupported claim appears in README/docs
- any private path or sensitive value appears
- any official/public ARC data would need to be copied into the repo
- the solver stops emitting exactly two outputs where required

## Owner actions required before actual submission
- Run the local validation commands above from the public checkout.
- Confirm the notebook/package bundle being uploaded contains only the approved execution files.
- Open the Kaggle submission notebook and verify the import bootstrap still resolves `src/`.
- Confirm the final uploaded bundle does not contain private files, tests, or docs.
- Submit manually only after the owner is satisfied with the notebook preview and packaging contents.
