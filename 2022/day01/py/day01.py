import sys


inp = sys.stdin.read()
elves = []
for i, elf in enumerate(inp.split("\n\n")):
    cals = 0
    for cal in elf.split("\n"):
        cals += int(cal)
    elves.append(cals)

print("Part 1:", max(elves))
print("Part 2:", sum(sorted(elves, reverse=True)[:3]))
