from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from typing import Iterable, List, Tuple

Pair = Tuple[int, int]


FREQS = Counter(a + b + c for a, b, c in product([1, 2, 3], repeat=3))


@dataclass(frozen=True)
class State:
    positions: Pair
    scores: Pair

    def __init__(self, positions: Iterable[int], scores: Iterable[int]):
        object.__setattr__(self, "positions", tuple(positions))
        object.__setattr__(self, "scores", tuple(scores))


def vadd(a: Pair, b: Pair) -> Pair:
    return (a[0] + b[0], a[1] + b[1])


def vmul(x: int, b: Pair) -> Pair:
    return (x * b[0], x * b[1])


def move(val: int, p: int, state: State) -> State:
    pos = list(state.positions)
    sco = list(state.scores)
    pos[p] = (pos[p] + val - 1) % 10 + 1
    sco[p] += pos[p]
    return State(pos, sco)


@lru_cache(maxsize=None)
def play(p: int, state: State) -> Pair:
    if state.scores[0] >= 21:
        return (1, 0)
    if state.scores[1] >= 21:
        return (0, 1)
    nextp = 1 if p == 0 else 0
    result = (0, 0)
    for val, freq in FREQS.items():
        played = play(nextp, move(val, p, state))
        result = vadd(result, vmul(freq, played))
    return result


def part1(positions: List[int]) -> int:
    MAX = 1000
    i = 0
    state = State(positions, [0, 0])

    while state.scores[0] < MAX and state.scores[1] < MAX:
        p = i % 2
        val = 3 * (3 * i + 1) + 3
        state = move(val, p, state)
        i += 1

    return next(s for s in state.scores if s < MAX) * i * 3


def part2(positions: List[int]) -> int:
    p1, p2 = play(0, State(positions, (0, 0)))
    return max(p1, p2)


if __name__ == "__main__":
    # problem = [4, 8]  # test
    problem = [8, 4]  # input

    print("Part 1:", part1(problem))
    print("Part 2:", part2(problem))
