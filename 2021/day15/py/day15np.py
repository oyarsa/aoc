import heapq
import sys
from itertools import product
from typing import Dict, List, Tuple, cast
import numpy as np

Pair = Tuple[int, int]
Graph = np.ndarray


def neighbours(v: Pair, n: int, m: int) -> List[Pair]:
    y, x = v
    ds = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    return [
        (yy, xx) for dx, dy in ds if 0 <= (yy := y + dy) < n and 0 <= (xx := x + dx) < m
    ]


def djikstra(graph):
    n, m = graph.shape
    dist: Dict[Pair, int] = {(0, 0): 0}
    pq: List[Tuple[int, Pair]] = []

    for v in np.ndindex(*graph.shape):
        v = cast(Pair, v)
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
    d = {
        (i, j): int(val)
        for i, line in enumerate(sys.stdin)
        for j, val in enumerate(line.strip())
    }
    n = max(y for y, _ in d.keys()) + 1
    m = max(x for _, x in d.keys()) + 1
    m = np.zeros((n, m), dtype=int)
    for (i, j), x in d.items():
        m[i, j] = x
    return m


def replicate_map(graph: Graph) -> Graph:
    n, m = graph.shape
    graph = np.pad(graph, ((0, 4 * n), (0, 4 * m)))
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
    n, m = problem.shape
    return dist[n - 1, m - 1]


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", solve(problem))
    print("Part 2:", solve(replicate_map(problem)))
