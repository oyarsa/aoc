from __future__ import annotations


def solve(problem: list[int], days: int) -> int:
    fishes = [0] * 9

    for f in problem:
        fishes[f] += 1

    for _ in range(days):
        fishes = fishes[1:] + fishes[:1]
        fishes[6] += fishes[8]

    return sum(fishes)


if __name__ == "__main__":
    problem = [int(x) for x in input().split(",")]
    print("part 1:", solve(problem, 80))
    print("part 2:", solve(problem, 256))
