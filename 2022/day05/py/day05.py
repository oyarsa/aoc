import copy
import itertools
import re
import sys


def splitstr(s, n=4):
    return [s[i : i + n] for i in range(0, len(s), n)]


def part1(stacks, instrs):
    for count, fro, to in instrs:
        for _ in range(count):
            el = stacks[fro - 1].pop()
            stacks[to - 1].append(el)
    return "".join(s[-1] for s in stacks)


def part2(stacks, instrs):
    for count, fro, to in instrs:
        els = stacks[fro - 1][-count:]
        stacks[fro - 1] = stacks[fro - 1][:-count]
        stacks[to - 1].extend(els)
    return "".join(s[-1] for s in stacks)


def main():
    stacks, instructions = sys.stdin.read().split("\n\n")
    stacks_lines = [splitstr(s) for s in stacks.splitlines()[:-1]]
    stacks_cols = list(map(list, itertools.zip_longest(*stacks_lines, fillvalue=None)))
    stacks = []
    for col in stacks_cols:
        new_col = []
        for x in col:
            if x is not None and x.strip():
                new_col.append(re.sub(r"\]|\[", "", x).strip())
        stacks.append(list(reversed(new_col)))

    move_re = r"move (\d+) from (\d+) to (\d+)"
    instrs = [
        [int(x) for x in re.findall(move_re, i)[0]] for i in instructions.splitlines()
    ]
    print("Part 1", part1(copy.deepcopy(stacks), instrs))
    print("Part 2", part2(stacks, instrs))


if __name__ == "__main__":
    main()
