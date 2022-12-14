import sys
from copy import deepcopy
from typing import NamedTuple


def parse_input():
    input = []
    for line in sys.stdin:
        coords_txt = line.split(" -> ")
        coords = [tuple(map(int, coord.split(","))) for coord in coords_txt]
        input.append(coords)
    return input


class Dimensions(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


def dimensions(input):
    min_x = min(x for line in input for x, _ in line)
    max_x = max(x for line in input for x, _ in line)
    max_y = max(y for line in input for _, y in line)
    return Dimensions(min_x, max_x, 0, max_y)


def input_to_grid(input, dim):
    max_x = dim.max_x - dim.min_x + 1
    max_y = dim.max_y - dim.min_y + 1

    grid = [["."] * max_x for _ in range(max_y)]

    for line in input:
        for (ax, ay), (bx, by) in zip(line, line[1:]):
            ax -= dim.min_x
            bx -= dim.min_x

            if ax == bx:
                if ay < by:
                    for y in range(ay, by + 1):
                        grid[y][ax] = "#"
                else:
                    for y in range(by, ay + 1):
                        grid[y][ax] = "#"
            elif ay == by:
                if ax < bx:
                    for x in range(ax, bx + 1):
                        grid[ay][x] = "#"
                else:
                    for x in range(bx, ax + 1):
                        grid[ay][x] = "#"

    return grid


def drop_sand(grid, starting_point):
    """Returns True if the sand stopped, False if it fell off the bottom or got blocked
    in the starting point."
    """
    x, y = starting_point
    grid[y][x] = "o"

    while True:
        if y + 1 >= len(grid):
            grid[y][x] = "."
            return False

        if grid[y + 1][x] == ".":
            new_x = x
        elif grid[y + 1][x - 1] == ".":
            new_x = x - 1
        elif grid[y + 1][x + 1] == ".":
            new_x = x + 1
        elif (x, y) == starting_point:
            return False
        else:
            return True

        new_y = y + 1

        if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid):
            grid[y][x] = "."
            return False

        grid[y][x] = "."
        grid[new_y][new_x] = "o"

        x, y = new_x, new_y


def extend_grid(grid, add_x):
    max_x = len(grid[0]) + add_x
    max_y = len(grid) + 2
    new_grid = [["."] * max_x for _ in range(max_y)]

    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            new_grid[i][j + add_x // 2] = char

    new_grid[max_y - 1] = "#" * max_x

    return new_grid


def solve(grid, starting_point):
    i = 0
    while True:
        stopped = drop_sand(grid, starting_point)
        if not stopped:
            return i
        i += 1


def main():
    input = parse_input()
    dim = dimensions(input)
    grid = input_to_grid(input, dim)

    starting_point = (500 - dim.min_x, 0)
    print("Part 1", solve(deepcopy(grid), starting_point))

    add_x = 2000
    new_grid = extend_grid(grid, add_x)
    starting_point = starting_point[0] + add_x // 2, starting_point[1]
    # +1 because the starting point is not counted
    print("Part 2", solve(new_grid, starting_point) + 1)


if __name__ == "__main__":
    main()
