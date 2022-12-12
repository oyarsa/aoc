import sys


def bfs(grid, start, end):
    len_x, len_y = len(grid[0]), len(grid)
    queue = [(start, start)]
    visited = {}

    while queue:
        (x, y), parent = queue.pop(0)
        if (x, y) in visited:
            continue

        visited[(x, y)] = parent

        if (x, y) == end:
            return visited

        neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for a, b in neighbours:
            if not (0 <= a < len_x and 0 <= b < len_y):
                continue
            if grid[b][a] > grid[y][x] + 1:
                continue
            queue.append(((a, b), (x, y)))

    return None


def backtrack(start, end, visited):
    current = end
    distance = 0
    while current != start:
        current = visited[current]
        distance += 1
    return distance


def find_nodes(grid, node):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == node:
                yield x, y


def part1(grid, start, end):
    visited = bfs(grid, start, end)
    distance = backtrack(start, end, visited)
    return distance


def part2(grid, end):
    min_dist = float("inf")
    starts = find_nodes(grid, ord("a"))
    for start in starts:
        if not (visited := bfs(grid, start, end)):
            continue
        distance = backtrack(start, end, visited)
        min_dist = min(min_dist, distance)
    return min_dist


def main():
    grid = [[ord(c) for c in line.strip()] for line in sys.stdin]

    start = next(find_nodes(grid, ord("S")))
    grid[start[1]][start[0]] = ord("a")

    end = next(find_nodes(grid, ord("E")))
    grid[end[1]][end[0]] = ord("z")

    print("Part 1:", part1(grid, start, end))
    print("Part 2:", part2(grid, end))


if __name__ == "__main__":
    main()
