from __future__ import annotations

import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.adj_list: defaultdict[str, list[str]] = defaultdict(list)

    def add(self, src: str, dst: str) -> None:
        self.adj_list[src].append(dst)
        self.adj_list[dst].append(src)

    def adj(self, node: str) -> list[str]:
        return self.adj_list[node]


def read_problem() -> Graph:
    graph = Graph()

    for line in sys.stdin:
        src, dst = line.strip().split("-")
        graph.add(src, dst)

    return graph


def recur_walk(graph: Graph, node: str, seen: set[str]) -> int:
    if node in seen:
        return 0
    if node == "end":
        return 1
    if node.islower():
        seen.add(node)

    return sum(recur_walk(graph, node, seen.copy()) for node in graph.adj(node))


def recur_walk2(graph: Graph, node: str, seen: set[str], double: bool) -> int:
    if node in seen:
        if double:
            return 0
        else:
            double = True
    if node == "end":
        return 1
    if node.islower():
        seen.add(node)

    return sum(
        recur_walk2(graph, node, seen.copy(), double)
        for node in graph.adj(node)
        if node != "start"
    )


def part1(problem: Graph) -> int:
    return recur_walk(problem, "start", set())


def part2(problem: Graph) -> int:
    return recur_walk2(problem, "start", set(), False)


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", part1(problem))
    print("Part 2:", part2(problem))
