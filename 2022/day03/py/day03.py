import sys


def priority(item_type: str):
    base = ord("A") if item_type.isupper() else ord("a")
    mod = 27 if item_type.isupper() else 1
    return ord(item_type) - base + mod


sacks = sys.stdin.read().splitlines()
prios = []
for sack in sacks:
    mid = len(sack) // 2
    first, second = set(sack[:mid]), set(sack[mid:])
    common = first & second
    prios.extend(priority(c) for c in common)

print("Part 1", sum(prios))

prios2 = []
for i in range(0, len(sacks), 3):
    group = sacks[i : i + 3]
    common = set.intersection(*map(set, group))
    prios2.extend(priority(c) for c in common)

print("Part 2", sum(prios2))
