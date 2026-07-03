# weslr-arc-agi2-submission

WESLR ARC-AGI-2 submission package with bundled solver code, reproducibility documentation, and no-internet evaluation support.

## Quick start
Clone the repository:
```bash
git clone https://github.com/pr0dus/weslr-arc-agi2-submission.git
cd weslr-arc-agi2-submission
```

Create an optional virtual environment:
```bash
python -m venv .venv
. .venv/bin/activate
```

Install the listed Python requirements:
```bash
python -m pip install -r requirements.txt
```

Run the bundled smoke test:
```bash
python -m pytest -q tests/test_dummy_no_data_smoke.py
```

The Kaggle submission JSON is a top-level dict keyed by `task_id`, and each task maps to a list of prediction objects containing `attempt_1` and `attempt_2` grids.

Optional import check, only if verified first:
```bash
PYTHONPATH=src python -c "import weslr_arc_solver; print('weslr_arc_solver import OK')"
```

The bundled fixture is dummy/no-data only. It is intended to verify package wiring, import isolation, and output formatting before evaluation packaging.

## Repository contents
- bundled solver code under `src/weslr_arc_solver`
- dummy/no-data smoke tests under `tests/`
- reproducibility, evaluation, and exclusion docs under `docs/`
- a submission notebook skeleton for packaging and review
- `.gitignore` for cache and build-artifact hygiene

## Evaluation constraints
- No internet during evaluation.
- No provider, model, or API calls.
- Only bundled source code.
- Exact two outputs per test input when required.
- Dummy/no-data fixtures are for smoke testing only.

## Validation
```bash
python -m pytest -q tests/test_dummy_no_data_smoke.py
```

## Reproducibility
See `docs/REPRODUCIBILITY.md` and `MANIFEST.sha256`.

## License
MIT — see `LICENSE`.
