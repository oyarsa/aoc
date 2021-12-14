from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass


@dataclass
class Problem:
    template: str
    rules: dict[tuple[str, str], str]


def read_problem() -> Problem:
    template, rules = sys.stdin.read().split("\n\n")
    new_pairs = {
        (a, b): c for (a, b), c in (rule.split(" -> ") for rule in rules.splitlines())
    }
    return Problem(template, new_pairs)


def solve(p: Problem, steps: int) -> int:
    total_counts = Counter(p.template)
    pair_counts = Counter(
        tuple(p.template[i : i + 2]) for i in range(len(p.template) - 1)
    )

    for _ in range(steps):
        new_pairs = pair_counts.copy()
        for (a, b), count in pair_counts.items():
            c = p.rules[a, b]
            new_pairs[a, c] += count
            new_pairs[c, b] += count
            new_pairs[a, b] -= count
            total_counts[c] += count
        pair_counts = new_pairs

    min_val = min(total_counts.values())
    max_val = max(total_counts.values())
    return max_val - min_val


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", solve(problem, 10))
    print("Part 2:", solve(problem, 40))
