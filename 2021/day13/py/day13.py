from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass

import numpy as np


@dataclass
class Problem:
    grid: np.ndarray
    folds: list[tuple[str, int]]
    max_x: int
    max_y: int


def read_problem() -> Problem:
    coords_input, folds_input = sys.stdin.read().split("\n\n")
    coords = [tuple(map(int, line.split(","))) for line in coords_input.splitlines()]

    max_x = max(x for x, _ in coords) + 1
    max_y = max(y for _, y in coords) + 1
    grid = np.full((max_y, max_x), ".")

    for x, y in coords:
        grid[y, x] = "#"

    folds: list[tuple[str, int]] = []
    for dir, number in re.findall(r"fold along ([xy])=(\d+)", folds_input):
        folds.append((dir, int(number)))

    return Problem(grid, folds, max_x, max_y)


def print_grid(p: Problem) -> None:
    for i in range(p.max_y):
        for j in range(p.max_x):
            char = "░" if p.grid[i, j] == "#" else " "
            print(char, end="")
        print()


def fold(problem: Problem, fold: tuple[str, int]) -> Problem:
    dir, num = fold
    fun = fold_x if dir == "x" else fold_y
    return fun(problem, num)


def fold_x(problem: Problem, col: int) -> Problem:
    for i in range(problem.max_y):
        for j in range(1, problem.max_x - col):
            if problem.grid[i, col - j] == ".":
                problem.grid[i, col - j] = problem.grid[i, col + j]

    problem.max_x = col
    return problem


def fold_y(problem: Problem, row: int) -> Problem:
    for i in range(1, problem.max_y - row):
        for j in range(problem.max_x):
            if problem.grid[row - i, j] == ".":
                problem.grid[row - i, j] = problem.grid[row + i, j]

    problem.max_y = row
    return problem


def do_folds(problem: Problem, n: int | None) -> Problem:
    for f in problem.folds[:n]:
        problem = fold(problem, f)
    return problem


def part1(problem: Problem) -> int:
    problem = do_folds(problem, n=1)
    return (problem.grid[: problem.max_y, : problem.max_x] == "#").sum()


def part2(problem: Problem) -> None:
    problem = do_folds(problem, n=None)
    print_grid(problem)


if __name__ == "__main__":
    problem = read_problem()
    start = time.perf_counter()
    print("Part 1:", part1(problem))
    print("Part 2:")
    part2(problem)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{elapsed}ms")
