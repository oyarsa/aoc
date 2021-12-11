import sys
from functools import reduce


def part1_score(line):
    matches = {"(": ")", "<": ">", "{": "}", "[": "]"}
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        elif char != matches[stack.pop()]:
            return scores[char]
    return 0


def part1(problem):
    return sum(part1_score(line) for line in problem)


def part2_score(line):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            stack.pop()

    score = reduce(lambda score, char: 5 * score + scores[char], reversed(stack), 0)
    return score


def part2(problem):
    incomplete = (line for line in problem if part1_score(line) == 0)
    scores = sorted(part2_score(line) for line in incomplete)
    return scores[len(scores) // 2]


if __name__ == "__main__":
    problem = list(line.strip() for line in sys.stdin)
    print("Part 1:", part1(problem))
    print("Part 2:", part2(problem))
