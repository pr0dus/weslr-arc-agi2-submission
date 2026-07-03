from __future__ import annotations

from copy import deepcopy
from typing import Any, Sequence


def copy_grid(grid: Sequence[Sequence[Any]]) -> list[list[Any]]:
    return [list(row) for row in deepcopy(grid)]


def invert_binary_grid(grid: Sequence[Sequence[Any]]) -> list[list[Any]]:
    inverted: list[list[Any]] = []
    for row in grid:
        new_row: list[Any] = []
        for cell in row:
            if cell == 0:
                new_row.append(1)
            elif cell == 1:
                new_row.append(0)
            else:
                new_row.append(cell)
        inverted.append(new_row)
    return inverted


def validate_grid(grid: Any) -> None:
    if not isinstance(grid, list) or not grid:
        raise ValueError("grid must be a non-empty list of rows")
    width = None
    for row in grid:
        if not isinstance(row, list) or not row:
            raise ValueError("grid rows must be non-empty lists")
        width = width or len(row)
        if len(row) != width:
            raise ValueError("grid must be rectangular")
