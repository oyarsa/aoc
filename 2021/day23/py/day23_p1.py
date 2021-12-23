from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache
from heapq import heappop, heappush
from sys import stdin

from icecream import ic  # NOQA

HALL = [0, 1, 5, 9, 13, 17, 18]
TYPES = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}
DEST = {
    0: [3, 4],
    1: [7, 8],
    2: [11, 12],
    3: [15, 16],
}
NEIGHBOURS = {
    0: [1],
    1: [0, 2],
    2: [1, 3, 5],
    3: [2, 4],
    4: [3],
    5: [2, 6],
    6: [5, 7, 9],
    7: [6, 8],
    8: [7],
    9: [6, 10],
    10: [9, 11, 13],
    11: [10, 12],
    12: [11],
    13: [10, 14],
    14: [13, 15, 17],
    15: [14, 16],
    16: [15],
    17: [14, 18],
    18: [17],
}
Positions = tuple[int]


@dataclass(frozen=True)
class State:
    cost: int
    positions: Positions

    def is_final(self) -> bool:
        final = (-1, -1, -1, 0, 0, -1, -1, 1, 1, -1, -1, 2, 2, -1, -1, 3, 3, -1, -1)
        return self.positions == final

    def __init__(self, cost: int, positions: Iterable[int]) -> None:
        object.__setattr__(self, "cost", cost)
        object.__setattr__(self, "positions", tuple(positions))

    def __lt__(self, other) -> bool:
        if not isinstance(other, State):
            raise TypeError("'<' only supported between instances of 'State'")
        return self.cost < other.cost


def read_problem() -> State:
    lines = stdin.read().split("\n")[2:-1]
    line1 = lines[0].replace("#", "")
    line2 = lines[1].strip().replace("#", "")

    positions = [-1] * 19

    for j, line in enumerate([line1, line2]):
        for i, x in enumerate(line):
            pos = 3 + i * 4 + j
            positions[pos] = TYPES[x]

    return State(0, positions)


def replace(pos: Positions, old: int, new: int, amphi: int) -> list[int]:
    new_pos = list(pos)
    new_pos[old] = -1
    new_pos[new] = amphi
    return new_pos


@cache
def calc_cost(pos: Positions, old: int, new: int, amphi: int) -> int:
    c = dfs(pos, old, new)
    return c * int(10 ** amphi)


def move(state: State, old_pos: int, new_pos: int, amphi: int) -> State:
    new_positions = replace(state.positions, old_pos, new_pos, amphi)
    new_cost = calc_cost(state.positions, old_pos, new_pos, amphi)
    return State(state.cost + new_cost, new_positions)


@cache
def is_valid(pos: Positions, i: int, j: int) -> bool:
    return dfs(pos, i, j) != -1


def dfs(pos: Positions, cur: int, dst: int) -> int:
    seen: set[int] = set()
    x = dfs_(seen, pos, cur, dst)
    return x


def dfs_(seen: set[int], pos: Positions, cur: int, dst: int) -> int:
    if cur == dst:
        return 0
    seen.add(cur)
    for nxt in NEIGHBOURS.get(cur, []):
        if pos[nxt] != -1 or nxt in seen:
            continue
        x = dfs_(seen, pos, nxt, dst)
        if x != -1:
            return 1 + x
    return -1


def djikstra(start: State) -> tuple[State, int] | None:
    dist: dict[State, int] = defaultdict(lambda: int(1e9), {start: 0})
    pq: list[State] = []

    dist[start] = 0
    heappush(pq, start)

    while pq:
        s = heappop(pq)
        if s.is_final():
            return s, dist[s]
        for v in possible_moves(s):
            alt = v.cost
            if alt < dist[v]:
                dist[v] = alt
                heappush(pq, v)
    return None


@cache
def possible_moves(state: State) -> Iterable[State]:
    pos = state.positions
    for i, a in enumerate(pos):
        if a == -1:
            continue

        x, y = DEST[a]
        if i == y or (i == x and pos[y] == a):
            continue

        if i not in HALL:
            for h in HALL:
                if pos[h] == -1 and is_valid(pos, i, h):
                    yield move(state, i, h, a)

        if pos[x] in [-1, a] and pos[y] in [-1, a]:
            if pos[x] == -1 and pos[y] != -1 and is_valid(pos, i, x):
                yield move(state, i, x, a)
            if pos[y] == -1 and is_valid(pos, i, y):
                yield move(state, i, y, a)


def print_game(s: State) -> None:
    c = {-1: ".", 0: "A", 1: "B", 2: "C", 3: "D"}
    print("Cost:", s.cost)
    print("#" * 13)

    print("#", end="")
    hall = sorted(HALL + [2, 6, 10, 14])
    for i in hall:
        print(c[s.positions[i]], end="")
    print("#")

    print("#" * 3, end="")
    for i in [3, 7, 11, 15]:
        print(c[s.positions[i]], end="#")
    print("#" * 2)

    print(" " * 2, end="")
    print("#", end="")
    for i in [4, 8, 12, 16]:
        print(c[s.positions[i]], end="#")
    print(" " * 2)

    print(" ", "#" * 9)


if __name__ == "__main__":
    p = read_problem()
    d = djikstra(p)
    if d:
        print_game(d[0])
        print(d[1])
