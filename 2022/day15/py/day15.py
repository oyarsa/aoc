import re
import sys
from collections import namedtuple

Point = namedtuple("Point", "x y")


def manhattan_dist(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def main():
    with open(sys.argv[1], "r") as file:
        sensors, beacons = read_input(file)
    y = int(sys.argv[2])
    max_coord = int(sys.argv[3])

    print("Part 1:", part1(sensors, beacons, y))
    print("Part 2:", part2(sensors, max_coord))


def read_input(file):
    regex = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    sensors = []
    beacons = set()

    for line in file:
        sx, sy, bx, by = map(int, re.findall(regex, line)[0])

        sensor = Point(sx, sy)
        beacon = Point(bx, by)

        sensors.append((sensor, manhattan_dist(sensor, beacon)))
        beacons.add(beacon)
    return sensors, beacons


def part1(sensors, beacons, y):
    max_x = max((s for s, _ in sensors), key=lambda p: p.x).x
    max_dist = max(d for _, d in sensors)

    count = 0
    for x in range(-max_dist, max_x + max_dist):
        p = Point(x, y)
        if p in beacons:
            continue
        for sensor, dist in sensors:
            if manhattan_dist(p, sensor) <= dist:
                count += 1
                break
    return count


def part2(sensors, max_coord):
    def check_pt(p):
        if p.x < 0 or p.y < 0 or p.x > max_coord or p.y > max_coord:
            return False
        for sensor, dist in sensors:
            if manhattan_dist(p, sensor) <= dist:
                return False
        return True

    for sensor, dist in sensors:
        for p in get_surrounding_points(sensor, dist):
            if check_pt(p):
                return p.x * 4000000 + p.y

    raise ValueError("No beacon found")


def get_surrounding_points(sensor, dist):
    "From https://is.gd/1TgW4k"
    x, y = sensor
    dist += 1

    yield Point(x, y + dist)
    yield Point(x, y - dist)
    for dx in range(1, dist):
        yield Point(x + dx, y + dist - dx)
        yield Point(x - dx, y + dist - dx)
        yield Point(x + dx, y - dist + dx)
        yield Point(x - dx, y - dist + dx)
    yield Point(x + dist, y)
    yield Point(x - dist, y)


if __name__ == "__main__":
    main()
