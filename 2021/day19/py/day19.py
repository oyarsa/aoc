from __future__ import annotations

from itertools import combinations, permutations, product
from sys import stdin

import numpy as np


def gen_rotation_matrices() -> list[np.ndarray]:
    # https://stackoverflow.com/a/70413438/5601342
    matrices: list[np.ndarray] = []
    for x, y, z in permutations([0, 1, 2]):
        for sx, sy, sz in product([-1, 1], repeat=3):
            m = np.zeros((3, 3))
            m[0, x] = sx
            m[1, y] = sy
            m[2, z] = sz
            if np.linalg.det(m) == 1:
                matrices.append(m)
    return matrices


ROTATIONS = gen_rotation_matrices()


def common(
    a: list[np.ndarray], b: list[np.ndarray]
) -> tuple[list[np.ndarray], np.ndarray] | None:
    set_a = set(map(tuple, a))

    for rot in ROTATIONS:
        b_rot = [rot @ v for v in b]
        for point_a in a:
            for point_b in b_rot:
                delta = np.array(point_a - point_b)
                new_b = [pb + delta for pb in b_rot]
                set_b = set(map(tuple, new_b))
                if len(set_a & set_b) >= 12:
                    return new_b, delta
    return None


def solve(scanners: list[list[np.ndarray]]) -> tuple[set[tuple], list[np.ndarray]]:
    n = len(scanners)

    normalised = {0: scanners[0]}
    deltas = [np.zeros(3)]
    left = set(range(n))

    while left:
        for i in range(n):
            if i not in normalised or i not in left:
                continue
            for j in range(n):
                if i == j or j in normalised:
                    continue
                result = common(normalised[i], scanners[j])
                if result is not None:
                    norm_beacons, delta = result
                    normalised[j] = norm_beacons
                    deltas.append(delta)
            left.remove(i)

    beacons = set(tuple(b) for scanner in normalised.values() for b in scanner)
    return beacons, deltas


def read_problem() -> list[list[np.ndarray]]:
    return [
        [np.fromiter(beacon.split(","), int) for beacon in scanner.splitlines()[1:]]
        for scanner in stdin.read().split("\n\n")
    ]


if __name__ == "__main__":
    problem = read_problem()
    beacons, deltas = solve(problem)
    print("Part 1:", len(beacons))
    maxd = max(np.abs(a - b).sum() for a, b in combinations(deltas, 2))  # type: ignore
    print("Part 2:", maxd)
