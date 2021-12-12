from __future__ import annotations

import sys
from collections import defaultdict
from typing import Optional


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

    count = sum(recur_walk(graph, node, seen.copy()) for node in graph.adj(node))
    if node in seen:
        seen.remove(node)
    return count


def recur_walk2(
    graph: Graph, node: str, seen: set[str], visited_twice: Optional[str]
) -> int:
    if node in seen:
        if visited_twice is not None:
            return 0
        else:
            visited_twice = node
    if node == "end":
        return 1
    if node.islower():
        seen.add(node)

    count = sum(
        recur_walk2(graph, node, seen, visited_twice)
        for node in graph.adj(node)
        if node != "start"
    )
    if node in seen and node != visited_twice:
        seen.remove(node)
    return count


def part1(problem: Graph) -> int:
    return recur_walk(problem, "start", set())


def part2(problem: Graph) -> int:
    return recur_walk2(problem, "start", set(), None)


if __name__ == "__main__":
    problem = read_problem()
    print("Part 1:", part1(problem))
    print("Part 2:", part2(problem))
