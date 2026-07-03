# WESLR ARC-AGI-2 Kaggle Execution Boundary Audit V1

## Current public repo HEAD
- `279b29a66e3e6bd9bd5073b65ce2eff62fa540fb`

## Roles by environment

### Android / Termux
- Authoring and control environment only.
- Used to edit the public repo, run local validation, and prepare packaging.
- Must not be assumed present inside Kaggle.

### GitHub public repo
- Public source and reproducibility host.
- Good for review, versioning, and local clone/push workflows.
- Not a scoring environment.
- Must not be assumed reachable from Kaggle scoring, especially with no internet.

### Kaggle notebook scoring environment
- Isolated execution environment for the actual run.
- No internet should be assumed.
- Must contain every runtime dependency needed for scoring before execution starts.
- Must not depend on Android paths, private WESLR paths, or GitHub fetches.

## No-internet consequence
If Kaggle cannot use the network, then the scoring notebook must already have:
- the runnable notebook code
- bundled source code
- any runtime-only files it needs
- a local output path

It cannot rely on:
- `git clone`
- PyPI installs from the network
- GitHub access during scoring
- private helper surfaces or private package paths
- private WESLR packages or hidden project files

## What must be present inside Kaggle before scoring
At minimum:
- the notebook code that starts the run
- the bundled `src/weslr_arc_solver/` package
- any runtime helper files imported by that package
- a local path bootstrap that resolves bundled source without internet
- a local output write path for the submission artifact

## Can the current public repo be used directly?
Not directly by GitHub URL during scoring.

Recommended interpretation:
- the public repo is the source-of-truth bundle
- it must be copied/uploaded into Kaggle as notebook files or a mounted Kaggle dataset
- Kaggle scoring should run from the uploaded files, not from live GitHub fetches

## Current notebook/package readiness
The current public skeleton is compatible with no-internet execution because it:
- imports only bundled source code
- has no provider/model/API/web calls
- writes a local `submission.json`
- uses a local-source bootstrap that prefers sibling `src/` or current working directory `src/`

The skeleton does not require Android-only paths.

## Does `submission_notebook_skeleton.py` assume Android/Termux-only paths?
No.
- It only checks for `src/` beside the file when available.
- It falls back to `Path.cwd() / "src"`.
- It does not reference hard-coded Android paths, private repo paths, or other private helper surfaces.

## Does any code assume internet, GitHub access, local private repo paths, or private packages?
No runtime code in the public package should rely on those things.
- Solver code imports from `weslr_arc_solver` only.
- The dummy smoke path is local and bundled.
- The skeleton does not call external services.
- The packaging doc and README stay public-facing.

## Cleanest no-internet Kaggle layout
### Recommended layout
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

### Runtime behavior
- The notebook starts in Kaggle.
- The bootstrap adds bundled `src/` to `sys.path`.
- The solver writes `submission.json` in the notebook working directory.
- No network or private path access is needed.

### Where `requirements.txt` fits
- Keep `requirements.txt` in the GitHub repo for local reproduction.
- Do not depend on it for Kaggle scoring unless all requirements are already available offline.
- For this package, runtime needs are already bundled or stdlib-only.

## Packaging options
### Option A — notebook upload with bundled files
- Upload the notebook code plus the `src/` tree into the Kaggle notebook workspace.
- Use the local bootstrap to resolve imports.
- Best when you want the simplest no-network execution path.

### Option B — Kaggle dataset attachment
- Publish or attach the bundle as a Kaggle dataset.
- Mount the dataset in the notebook and add the mounted `src/` to `sys.path`.
- Useful if you want a reusable artifact, but it adds one more indirection.

## Recommended packaging option
- **Option A** is recommended for this repo.
- It keeps the execution boundary simple: notebook + sibling `src/` + local output file.
- It matches the current skeleton's bootstrap behavior.

## Exact files needed inside Kaggle
Runtime minimum:
- `submission_notebook_skeleton.py` (or its notebook-cell equivalent)
- `src/weslr_arc_solver/__init__.py`
- `src/weslr_arc_solver/adapter.py`
- `src/weslr_arc_solver/emitter.py`
- `src/weslr_arc_solver/grid.py`
- `src/weslr_arc_solver/public_gate.py`
- `src/weslr_arc_solver/redaction.py`
- `src/weslr_arc_solver/schema.py`
- `src/weslr_arc_solver/scorer.py`
- `src/weslr_arc_solver/solver.py`

Useful only for local review, not needed at Kaggle scoring time:
- `requirements.txt`
- `README.md`
- `docs/*`
- `tests/*`
- `MANIFEST.sha256`
- `LICENSE`
- `NOTICE.md`
- `EXPORT_AUDIT.md`
- `EXPORT_REPORT.md`

## Exact files not needed inside Kaggle
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
- private WESLR files, private paths, or sensitive values
- any official/public ARC data files not already part of the public repo

## Owner actions needed after joining the competition
1. Open the Kaggle competition workspace.
2. Create a notebook or notebook-equivalent run environment.
3. Upload/attach the public bundle files.
4. Confirm the notebook can import `weslr_arc_solver` without internet.
5. Run a dry notebook execution and inspect `submission.json`.
6. Verify the file layout before any real submission.
7. Submit manually only after the notebook preview and file bundle look correct.

## What should be tested first in Kaggle without submitting?
1. Import bootstrap resolves bundled source.
2. `weslr_arc_solver` imports successfully.
3. The run produces a local `submission.json`.
4. The notebook does not try to use network, GitHub, or private paths.
5. The output format matches the expected local submission shape.

## Blockers before real submission
- notebook cannot see bundled `src/`
- any code path needs internet or GitHub
- any code path needs private WESLR or Android-only paths
- any unsupported claim wording appears in repo/docs
- any official/public ARC data would need to be copied into the repo
- the notebook cannot generate its local output artifact cleanly

## Next recommended lane
- Build a Kaggle-ready notebook bundle from the public repo layout and test the notebook preview locally before any real submission.
