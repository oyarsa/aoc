import sys


def find_marker(line, n):
    for i in range(n, len(line)):
        chars = line[i - n : i]
        if len(set(chars)) == n:
            return i


line = sys.stdin.readline()
print("Part 1", find_marker(line, 4))
print("Part 2", find_marker(line, 14))
