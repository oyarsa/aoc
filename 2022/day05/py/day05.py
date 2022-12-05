import copy
import itertools
import re
import sys


def splitstr(s, n=4):
    return [s[i : i + n] for i in range(0, len(s), n)]


stacks, instructions = sys.stdin.read().split("\n\n")
# stacks = stacks.replace("[", "").replace("]", "")
# print(stacks)
# stacks_lines = [s.split(" ") for s in stacks.splitlines()[:-1]]
stacks_lines = [splitstr(s) for s in stacks.splitlines()[:-1]]
# print(stacks_lines)
stacks_cols = list(map(list, itertools.zip_longest(*stacks_lines, fillvalue=None)))
stacks = []
for col in stacks_cols:
    new_col = []
    for x in col:
        if x is not None and x.strip():
            # new_col.append(x.replace("]", "").replace("[", ""))
            new_col.append(re.sub(r"\]|\[", "", x).strip())
    stacks.append(list(reversed(new_col)))

instrs = [
    list(map(int, re.findall(r"move (\d+) from (\d+) to (\d+)", i)[0]))
    for i in instructions.splitlines()
]

stackscopy = copy.deepcopy(stacks)
for count, fro, to in instrs:
    for i in range(count):
        el = stackscopy[fro - 1].pop()
        stackscopy[to - 1].append(el)

print("Part 1", "".join(s[-1] for s in stackscopy))

for count, fro, to in instrs:
    els = stacks[fro - 1][-count:]
    # print(stacks[fro - 1], stacks[fro - 1])
    # print(count, fro, to, els)
    stacks[fro - 1] = stacks[fro - 1][:-count]
    # print(stacks[fro - 1])
    stacks[to - 1].extend(els)
    # print(stacks[to - 1])
    # print()


print("Part 2", "".join(s[-1] for s in stacks))
