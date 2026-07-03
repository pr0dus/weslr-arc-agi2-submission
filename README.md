# weslr-arc-agi2-submission

WESLR ARC-AGI-2 submission package with bundled solver code, reproducibility documentation, and no-internet evaluation support.

## Repository contents
- bundled solver code under `src/weslr_arc_solver`
- dummy/no-data smoke tests under `tests/`
- reproducibility, evaluation, and exclusion docs under `docs/`
- a submission notebook skeleton for packaging and review

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
