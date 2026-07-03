"""Submission notebook skeleton.

Intended Kaggle flow:
- load Kaggle-provided input paths only
- run with no internet
- import only bundled source code from this public package
- emit exactly two outputs per ARC-AGI-2 test input when required
- write submission file in Kaggle-required format
- no agent/model/provider/API calls
- no manual repair after execution starts
"""

from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_local_src() -> None:
    """Make the bundled `src/` package importable in a Kaggle-style checkout."""

    candidates = []
    try:
        candidates.append(Path(__file__).resolve().parent / "src")
    except NameError:
        pass
    candidates.append(Path.cwd() / "src")

    for src_dir in candidates:
        if src_dir.exists() and str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
            return


_bootstrap_local_src()

from weslr_arc_solver.solver import run_submission_skeleton


if __name__ == "__main__":
    run_submission_skeleton()
