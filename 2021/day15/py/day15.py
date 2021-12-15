import heapq
import sys
from itertools import product
from typing import Dict, List, Tuple

Pair = Tuple[int, int]
Graph = Dict[Pair, int]


def neighbours(v: Pair, n: int, m: int) -> List[Pair]:
    y, x = v
    ds = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    return [
        (yy, xx) for dx, dy in ds if 0 <= (yy := y + dy) < n and 0 <= (xx := x + dx) < m
    ]


def get_n_m(graph: Graph) -> Pair:
    n = max(y for y, _ in graph.keys()) + 1
    m = max(x for _, x in graph.keys()) + 1
    return n, m


def djikstra(graph):
    n, m = get_n_m(graph)
    dist: Dict[Pair, int] = {(0, 0): 0}
    pq: List[Tuple[int, Pair]] = []

    for v in graph.keys():
        if v != (0, 0):
            dist[v] = int(1e9)
        heapq.heappush(pq, (dist[v], v))

    while pq:
        _, u = heapq.heappop(pq)
        for v in neighbours(u, n, m):
            alt = dist[u] + graph[v]
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(pq, (alt, v))
    return dist


def read_problem() -> Graph:
    return {
        (i, j): int(val)
        for i, line in enumerate(sys.stdin)
        for j, val in enumerate(line.strip())
    }


def replicate_map(graph: Graph) -> Graph:
    graph = graph.copy()
    n, m = get_n_m(graph)
    for a, b, i, j in product(range(5), range(5), range(n), range(m)):
        new = a + b + graph[i, j]
        if new > 9:
            new -= 9
        ii = n * (a) + i
        jj = m * (b) + j
        graph[ii, jj] = new

    return graph


def solve(problem: Graph) -> int:
    dist = djikstra(problem)
    n, m = get_n_m(problem)
    return dist[n - 1, m - 1]


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", solve(problem))
    print("Part 2:", solve(replicate_map(problem)))
