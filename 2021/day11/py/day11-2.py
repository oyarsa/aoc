"""Day 11 using recursion."""
import sys
import itertools

D = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def read_problem():
    return {
        (x, y): v
        for y, line in enumerate(sys.stdin)
        for x, v in enumerate(map(int, line.strip()))
    }


def inc_and_flash(problem, x, y):
    if (x, y) not in problem or problem[x, y] == 10:
        return 0

    problem[x, y] += 1
    if problem[x, y] != 10:
        return 0

    return 1 + sum(inc_and_flash(problem, x + dx, y + dy) for dx, dy in D)


def reset(problem):
    for x, y in problem:
        if problem[x, y] == 10:
            problem[x, y] = 0


def do_step(problem):
    flashes = sum(inc_and_flash(problem, x, y) for x, y in problem)
    reset(problem)
    return flashes


def part1(problem, steps):
    return sum(do_step(problem) for _ in range(steps))


def part2(problem):
    return next(i for i in itertools.count(1) if do_step(problem) == 100)


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", part1(problem.copy(), 100))
    print("Part 2:", part2(problem.copy()))
