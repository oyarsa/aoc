from __future__ import annotations

import re
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Probe(NamedTuple):
    xvel: int
    yvel: int
    pos: Point


class Target(NamedTuple):
    bl: Point  # Bottom-left
    tr: Point  # Top-right


def read_problem(line: str) -> Target:
    match = re.findall(r".*x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", line)
    x1, x2, y1, y2 = map(int, match[0])
    x1, y1 = min(x1, x2), min(y1, y2)
    x2, y2 = max(x1, x2), max(y1, y2)
    return Target(Point(x1, y1), Point(x2, y2))


def step(p: Probe) -> Probe:
    xvel, yvel, (x, y) = p
    x += xvel
    y += yvel
    xvel = max(xvel - 1, 0)
    yvel -= 1
    return Probe(xvel, yvel, Point(x, y))


def simulate(p: Probe, t: Target) -> int | None:
    max_ypos = 0
    while p.pos.x <= t.tr.x and p.pos.y >= t.bl.y:
        max_ypos = max(max_ypos, p.pos.y)
        if t.bl.x <= p.pos.x <= t.tr.x and t.bl.y <= p.pos.y <= t.tr.y:
            return max_ypos
        p = step(p)
    return None


def solve(tgt: Target) -> list[int]:
    hits: list[int] = []

    for xvel in range(tgt.tr.x + 1):
        for yvel in range(tgt.bl.y, -tgt.bl.y + 1):
            p = Probe(xvel, yvel, Point(0, 0))
            if (r := simulate(p, tgt)) is not None:
                hits.append(r)

    return hits


def part1(tgt: Target) -> int:
    return max(solve(tgt))


def part2(tgt: Target) -> int:
    return len(solve(tgt))


if __name__ == "__main__":
    # problem = read_problem("target area: x=20..30, y=-10..-5")  # test
    problem = read_problem("target area: x=60..94, y=-171..-136")  # input
    print("Part 1:", part1(problem))
    print("Part 2:", part2(problem))
