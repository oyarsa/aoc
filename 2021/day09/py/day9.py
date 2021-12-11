from __future__ import annotations

import sys
from itertools import product

import numpy as np

D = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def find_lowest_points(problem: np.ndarray) -> list[tuple[int, int]]:
    n, m = problem.shape
    lowest = [
        (i, j)
        for i, j in product(range(1, n - 1), range(1, m - 1))
        if problem[i, j] < min(problem[i + dy, j + dx] for dx, dy in D)
    ]
    return lowest


def part1(problem: np.ndarray) -> int:
    return sum(problem[i, j] + 1 for i, j in find_lowest_points(problem))


def search(problem: np.ndarray, i: int, j: int):
    if problem[i, j] == 9:
        return 0
    problem[i, j] = 9
    return 1 + sum(search(problem, i + dy, j + dx) for dx, dy in D)


def part2(problem: np.ndarray) -> int:
    basins = sorted(search(problem, i, j) for i, j in find_lowest_points(problem))
    a, b, c = basins[-3:]
    return a * b * c


if __name__ == "__main__":
    rows = [list(line.strip()) for line in sys.stdin]
    problem = np.pad(np.array(rows, dtype="int"), (1, 1), "maximum")
    print("Part 1:", part1(problem))
    print("Part 2:", part2(problem))
