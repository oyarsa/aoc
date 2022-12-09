import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def dist(a: Point, b: Point) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y))


n_knots = 10


def print_path(path: list[list[Point]]) -> None:
    max_x = 6
    max_y = 4
    knots = path[-1]

    for y in range(max_y, -1, -1):
        for x in range(max_x):
            char = "."
            for i in range(n_knots - 1, -1, -1):
                if Point(x, y) == knots[i]:
                    char = str(i)
            print(char, end="")
        print()

    print()
    print()


instructions = sys.stdin.read().splitlines()

knots = [Point(0, 0) for _ in range(n_knots)]
visited = {knots[-1]}

path = [knots]
print_path(path)

for instruction in instructions:
    direction, steps = instruction[0], int(instruction[1:])

    # print(instruction)
    for step in range(steps):
        head = knots[0]
        if direction == "R":
            head = Point(head.x + 1, head.y)
        elif direction == "L":
            head = Point(head.x - 1, head.y)
        elif direction == "U":
            head = Point(head.x, head.y + 1)
        elif direction == "D":
            head = Point(head.x, head.y - 1)
        knots[0] = head

        for i in range(n_knots - 1):
            head, tail = knots[i], knots[i + 1]

            if head == tail or dist(head, tail) == 1:
                pass
            # same column
            elif head.x == tail.x:
                # head is below tail
                if head.y < tail.y:
                    tail = Point(tail.x, tail.y - 1)
                # head is above tail
                else:
                    tail = Point(tail.x, tail.y + 1)
            # same row
            elif head.y == tail.y:
                # head is to the right of tail
                if head.x > tail.x:
                    tail = Point(tail.x + 1, tail.y)
                # head is to the left of tail
                else:
                    tail = Point(tail.x - 1, tail.y)
            # neither
            else:
                # head is to the right of and above tail
                if head.x > tail.x and head.y > tail.y:
                    tail = Point(tail.x + 1, tail.y + 1)
                # head is to the left of and above tail
                elif head.x < tail.x and head.y > tail.y:
                    tail = Point(tail.x - 1, tail.y + 1)
                # head is to the right of and below tail
                elif head.x > tail.x and head.y < tail.y:
                    tail = Point(tail.x + 1, tail.y - 1)
                # head is to the left of and below tail
                else:
                    tail = Point(tail.x - 1, tail.y - 1)
            knots[i], knots[i + 1] = head, tail

        path.append(knots)
        visited.add(knots[-1])
        print_path(path)

print("Part 1", len(visited))


def print_visited(visited):
    for y in range(4, -1, -1):
        for x in range(6):
            if Point(x, y) in visited:
                print("#", end="")
            else:
                print(".", end="")
        print()

    print()
    print()


# print_visited(visited)
