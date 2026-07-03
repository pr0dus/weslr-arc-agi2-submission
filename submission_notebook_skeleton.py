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

from weslr_arc_solver.solver import run_submission_skeleton


if __name__ == "__main__":
    run_submission_skeleton()
