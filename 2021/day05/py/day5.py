from __future__ import annotations

import re
import sys
from typing import Match, Tuple, cast

import numpy as np

Coord = Tuple[int, int]
Line = Tuple[Coord, Coord]
Matrix = np.ndarray


def read_problem() -> list[Line]:
    lines: list[Line] = []
    for line in sys.stdin:
        matches = cast(Match[str], re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line))
        x1, y1, x2, y2 = map(int, matches.groups())
        lines.append(((x1, y1), (x2, y2)))
    return lines


def fill_lines(m: Matrix, line: Line, diagonal: bool = False) -> Matrix:
    (x1, y1), (x2, y2) = min(*line), max(*line)

    if x1 == x2:
        y1, y2 = min(y1, y2), max(y1, y2)
        m[y1 : y2 + 1, x1] += 1
    elif y1 == y2:
        x1, x2 = min(x1, x2), max(x1, x2)
        m[y1, x1 : x2 + 1] += 1
    elif diagonal:
        step = 1 if y1 < y2 else -1
        for i in range(abs(y1 - y2) + 1):
            m[y1 + i * step, x1 + i] += 1

    return m


def solve(lines: list[Line], part: int) -> int:
    dim = np.array(lines).max() + 1
    mat = np.zeros((dim, dim), dtype=int)
    for line in lines:
        mat = fill_lines(mat, line, diagonal=part == 2)
    return (mat >= 2).sum()


if __name__ == "__main__":
    lines = read_problem()
    print("Part 1:", solve(lines, part=1))
    print("Part 2:", solve(lines, part=2))
