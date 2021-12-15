import sys
from heapq import heappop, heappush
from itertools import product
from typing import Dict, List, Tuple

Pair = Tuple[int, int]
Graph = Dict[Pair, int]


def neighbours(v: Pair) -> List[Pair]:
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    return [(v[0] + dy, v[1] + dx) for dx, dy in directions]


def get_n_m(graph: Graph) -> Pair:
    n = max(y for y, _ in graph.keys()) + 1
    m = max(x for _, x in graph.keys()) + 1
    return n, m


def djikstra(graph: Graph, start: Pair, end: Pair) -> Dict[Pair, int]:
    dist: Dict[Pair, int] = {start: 0}
    pq: List[Tuple[int, Pair]] = []

    for v in graph.keys():
        if v != start:
            dist[v] = int(1e9)
        heappush(pq, (dist[v], v))

    while pq:
        _, u = heappop(pq)
        if u == end:
            return dist
        for v in neighbours(u):
            if v not in graph:
                continue
            alt = dist[u] + graph[v]
            if alt < dist[v]:
                dist[v] = alt
                heappush(pq, (alt, v))
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
    for ix, jx, i, j in product(range(5), range(5), range(n), range(m)):
        graph[ix * n + i, jx * m + j] = (ix + jx + graph[i, j] - 1) % 9 + 1

    return graph


def solve(problem: Graph) -> int:
    n, m = get_n_m(problem)
    start, end = (0, 0), (n - 1, m - 1)
    dist = djikstra(problem, start, (n - 1, m - 1))
    return dist[end]


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", solve(problem))
    print("Part 2:", solve(replicate_map(problem)))
