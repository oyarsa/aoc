from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from heapq import heappop, heappush
from sys import stdin

from icecream import ic  # NOQA
from rich.console import Console

HALL = [0, 1, 5, 9, 13, 17, 18]
TYPES = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}
# fmt: off
DEST = [
    [3, 4, 19, 20],    # 0 (A)
    [7, 8, 21, 22],    # 1 (B)
    [11, 12, 23, 24],  # 2 (C)
    [15, 16, 25, 26],  # 3 (D)
]
NEIGHBOURS = [
    [1],            # 0
    [0, 2],         # 1
    [1, 3, 5],      # 2
    [2, 4],         # 3
    [3, 19],        # 4
    [2, 6],         # 5
    [5, 7, 9],      # 6
    [6, 8],         # 7
    [7, 21],        # 8
    [6, 10],        # 9
    [9, 11, 13],    # 10
    [10, 12],       # 11
    [11, 23],       # 12
    [10, 14],       # 13
    [13, 15, 17],   # 14
    [14, 16],       # 15
    [15, 25],       # 16
    [14, 18],       # 17
    [17],           # 18
    [4, 20],        # 19
    [19],           # 20
    [8, 22],        # 21
    [21],           # 22
    [12, 24],       # 23
    [23],           # 24
    [16, 26],       # 25
    [25],           # 26
]
# fmt: on

Index = int
Amphi = int
Positions = tuple[Amphi, ...]


@dataclass(frozen=True)
class State:
    cost: int
    positions: Positions

    def is_final(self) -> bool:
        p = self.positions
        # fmt: off
        return p == (
            -1, -1, -1, 0, 0, -1, -1, 1, 1, -1, -1, 2, 2, -1, -1, 3, 3, -1, -1,
            0, 0, 1, 1, 2, 2, 3, 3
        )
        # fmt: on

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost


def replace(pos: Positions, old: Index, new: Index, amphi: Amphi) -> Positions:
    new_pos = list(pos)
    new_pos[old] = -1
    new_pos[new] = amphi
    return tuple(new_pos)


def calc_cost(pos: Positions, old: Index, new: Index, amphi: Amphi) -> int:
    c = dfs(pos, old, new)
    assert c is not None
    return c * int(10 ** amphi)


def move(state: State, old_pos: Index, new_pos: Index, amphi: Amphi) -> State:
    return State(
        cost=state.cost + calc_cost(state.positions, old_pos, new_pos, amphi),
        positions=replace(state.positions, old_pos, new_pos, amphi),
    )


def is_valid(pos: Positions, i: Index, j: Index) -> bool:
    return dfs(pos, i, j) is not None


def dfs(pos: Positions, cur: Index, dst: Index) -> int | None:
    return dfs_(set(), pos, cur, dst)


def dfs_(seen: set[int], pos: Positions, cur: Index, dst: Index) -> int | None:
    if cur == dst:
        return 0
    seen.add(cur)
    for nxt in NEIGHBOURS[cur]:
        if pos[nxt] != -1 or nxt in seen:
            continue
        if (x := dfs_(seen, pos, nxt, dst)) is not None:
            return 1 + x
    return None


def djikstra(start: State) -> State | None:
    dist: dict[State, int] = defaultdict(lambda: int(1e9), {start: 0})
    pq: list[State] = []

    dist[start] = 0
    heappush(pq, start)

    while pq:
        s = heappop(pq)
        if s.is_final():
            return s
        for v in possible_moves(s):
            alt = v.cost
            if alt < dist[v]:
                dist[v] = alt
                heappush(pq, v)
    return None


def possible_moves(state: State) -> Iterable[State]:
    pos = state.positions
    for i, amphi in enumerate(pos):
        if amphi == -1:
            continue

        room = DEST[amphi]

        # If the current position is in a room and everyone below is the same type,
        # we don't want to move.
        if any(
            i == room[j] and all(pos[room[k]] == amphi for k in range(j + 1, len(room)))
            for j in range(len(room))
        ):
            continue

        # We won't move in the hall if we're already there
        if i not in HALL:
            for h in HALL:
                if pos[h] == -1 and is_valid(pos, i, h):
                    yield move(state, i, h, amphi)

        # We'll only enter a room if the spot doesn't have any amphis from other types
        for j in range(len(room)):
            if (
                pos[room[j]] == -1
                and all(pos[room[k]] == amphi for k in range(j + 1, len(room)))
                and is_valid(pos, i, room[j])
            ):
                yield move(state, i, room[j], amphi)


def print_game(s: State) -> None:
    def h(n: int = 1) -> str:
        return "[black]#[/black]" * n

    def p(idxs: Iterable[int], sep: str = h()) -> str:
        c = {
            -1: "[cyan]·[/cyan]",
            0: "[yellow]A[/yellow]",
            1: "[green]B[/green]",
            2: "[red]C[/red]",
            3: "[purple]D[/purple]",
        }
        return sep.join(c[s.positions[i]] for i in idxs)

    console = Console()
    console.print("Cost:", s.cost)
    console.print(h(13))

    hall = sorted(HALL + [2, 6, 10, 14])
    console.print(f"{h()}{p(hall, '')}{h()}")
    top = [3, 7, 11, 15]
    console.print(f"{h(3)}{p(top)}{h(3)}")

    bot_rows = [[4, 8, 12, 16], [19, 21, 23, 25], [20, 22, 24, 26]]
    for row in bot_rows:
        console.print(f"  {h()}{p(row)}{h()}")

    console.print(" ", h(9))


def read_problem() -> State:
    lines = stdin.read().split("\n")[2:-1]
    rows = [line.strip().replace("#", "") for line in lines]

    positions = [-1] * 27

    for j, line in enumerate(rows[:2]):
        for i, x in enumerate(line):
            pos = 3 + 4 * i + j
            positions[pos] = TYPES[x]

    for j, line in enumerate(rows[2:]):
        for i, x in enumerate(line):
            pos = 19 + 2 * i + j
            positions[pos] = TYPES[x]

    print(positions)

    return State(0, tuple(positions))


if __name__ == "__main__":
    p = read_problem()
    print_game(p)

    if d := djikstra(p):
        print_game(d)
