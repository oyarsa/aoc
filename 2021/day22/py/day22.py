from __future__ import annotations

import re
from itertools import product
from sys import stdin
from typing import NamedTuple


class Cube(NamedTuple):
    x: range
    y: range
    z: range

    def volume(self) -> int:
        vol = 1
        for c in self:
            vol *= c.stop - c.start
        return vol

    def intersect(self, c2: Cube) -> Cube | None:
        intersections: list[range] = []
        for a, b in zip(self, c2):
            if overlap := find_overlap(a, b):
                intersections.append(overlap)
            else:
                return None
        return Cube(*intersections)


class Cuboid(NamedTuple):
    toggle: bool
    cube: Cube


Problem = list[Cuboid]


def find_overlap(c1: range, c2: range) -> range | None:
    if (
        c1.start <= c2.start < c1.stop
        or c2.start <= c1.start < c2.stop
        or c1.start < c2.stop <= c1.stop
        or c2.start < c1.stop <= c2.stop
    ):
        points = sorted((c1.start, c1.stop - 1, c2.start, c2.stop - 1))
        return range(points[1], points[2] + 1)
    return None


def toggle_all(cuboids: list[Cuboid]) -> int:
    on: list[Cube] = []
    off: list[Cube] = []
    volume = 0

    for toggle, cube in cuboids:
        num_on, num_off = len(on), len(off)

        if toggle:
            volume += cube.volume()
            on.append(cube)

        for i in range(num_on):
            intersect = cube.intersect(on[i])
            if intersect:
                volume -= intersect.volume()
                off.append(intersect)

        for i in range(num_off):
            intersect = cube.intersect(off[i])
            if intersect:
                volume += intersect.volume()
                on.append(intersect)
    return volume


def read_problem() -> list[Cuboid]:
    cuboids: list[Cuboid] = []

    for line in stdin:
        matches = re.findall(
            r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
        )
        toggle, *coords = matches[0]
        x1, x2, y1, y2, z1, z2 = map(int, coords)
        cuboids.append(
            Cuboid(
                toggle == "on",
                Cube(range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1)),
            )
        )

    return cuboids


def part1(problem: Problem) -> int:
    points = set()

    for toggle, cube in problem:
        if any(c.start < -50 or c.stop > 51 for c in cube):
            continue

        for point in product(cube.x, cube.y, cube.z):
            if toggle:
                points.add(point)
            else:
                points.discard(point)

    return len(points)


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", part1(problem))
    print("Part 1:", toggle_all(problem))
