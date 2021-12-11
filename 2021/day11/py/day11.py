"""Day 11 with a queue (deque)."""
import sys
import itertools
from collections import deque

D = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def read_problem():
    return {
        (x, y): v
        for y, line in enumerate(sys.stdin)
        for x, v in enumerate(map(int, line.strip()))
    }


def do_step(problem):
    next = deque(problem.keys())
    while next:
        x, y = next.popleft()
        if (x, y) in problem:
            problem[x, y] += 1
            if problem[x, y] == 10:
                next.extend((x + dx, y + dy) for dx, dy in D)

    flashes = 0
    for x, y in problem.keys():
        if problem[x, y] >= 10:
            problem[x, y] = 0
            flashes += 1
    return flashes


def part1(problem, steps):
    return sum(do_step(problem) for _ in range(steps))


def part2(problem):
    return next(i for i in itertools.count(1) if do_step(problem) == 100)


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", part1(problem.copy(), 100))
    print("Part 2:", part2(problem.copy()))
