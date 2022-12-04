import sys
import re


def contains(x1, y1, x2, y2):
    return x1 <= x2 and y1 >= y2


def overlaps(x1, y1, x2, y2):
    a = max(x1, x2)
    b = min(y1, y2)
    return a <= b


assignments = []
for line in sys.stdin:
    matches = re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", line)[0]
    assignments.append(list(map(int, matches)))

contained = 0
for a, b, c, d in assignments:
    contained += contains(a, b, c, d) or contains(c, d, a, b)

print("Part 1", contained)

overlap = 0
for a, b, c, d in assignments:
    overlap += overlaps(a, b, c, d)

print("Part 2", overlap)
