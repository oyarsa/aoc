from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass
from functools import reduce
from typing import Set, Tuple

Grid = Set[Tuple[int, int]]


@dataclass
class Problem:
    grid: Grid
    folds: list[tuple[str, int]]


def read_problem() -> Problem:
    coords_input, folds_input = sys.stdin.read().split("\n\n")

    grid = {
        (x, y)
        for x, y in (map(int, line.split(",")) for line in coords_input.splitlines())
    }

    folds = [
        (dir, int(number))
        for dir, number in re.findall(r"fold along ([xy])=(\d+)", folds_input)
    ]

    return Problem(grid, folds)


def print_grid(grid: Grid) -> None:
    max_x, max_y = map(max, zip(*grid))
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            char = "░" if (x, y) in grid else " "
            print(char, end="")
        print()


def fold(grid: Grid, fold: tuple[str, int]) -> Grid:
    dir, pos = fold
    if dir == "y":
        return {(x, 2 * pos - y) if y > pos else (x, y) for x, y in grid}
    else:
        return {(2 * pos - x, y) if x > pos else (x, y) for x, y in grid}


def do_folds(problem: Problem, n: int | None) -> Grid:
    return reduce(fold, problem.folds[:n], problem.grid)


def part1(problem: Problem) -> int:
    grid = do_folds(problem, n=1)
    return len(grid)


def part2(problem: Problem) -> None:
    grid = do_folds(problem, n=None)
    print_grid(grid)


if __name__ == "__main__":
    problem = read_problem()
    start = time.perf_counter()

    print("Part 1:", part1(problem))
    print("Part 2:")
    part2(problem)

    elapsed = (time.perf_counter() - start) * 1000
    print(f"{elapsed}ms")
