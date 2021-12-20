from __future__ import annotations

import sys

import numpy as np


def read_problem() -> tuple[np.ndarray, np.ndarray]:
    algo, image_txt = sys.stdin.read().split("\n\n")
    algo = np.where(np.array(list(algo)) == "#", "1", "0")
    image = [list(line.strip()) for line in image_txt.splitlines()]
    image = np.where(np.array(image) == "#", "1", "0")
    return algo, image


def enhance(image: np.ndarray, algo: np.ndarray, fill: str) -> np.ndarray:
    image = np.pad(image, 2, constant_values=fill)
    n, m = image.shape
    new = np.full((n, m), fill, dtype="str")

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            neighbours = image[i - 1 : i + 2, j - 1 : j + 2].flatten()
            idx = int("".join(neighbours), 2)
            new[i, j] = str(algo[idx])

    return new[1 : n - 1, 1 : m - 1]


def solve(image: np.ndarray, algo: np.ndarray, n: int) -> int:
    for i in range(n):
        if algo[0] == "0":
            fill = "0"
        else:
            fill = "0" if i % 2 == 0 else "1"
        image = enhance(image, algo, fill)
    return (image == "1").sum()


if __name__ == "__main__":
    algo, image = read_problem()
    print("Part 1:", solve(image, algo, 2))
    print("Part 2:", solve(image, algo, 50))
