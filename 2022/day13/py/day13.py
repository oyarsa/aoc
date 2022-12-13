import sys
from ast import literal_eval
from functools import cmp_to_key


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if left > right:
            return 1
        return 0

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    if not left and right:
        return -1
    if left and not right:
        return 1
    if not left and not right:
        return 0

    r = compare(left[0], right[0])
    if r == 0:
        return compare(left[1:], right[1:])
    return r


def is_correct(left, right):
    return compare(left, right) == -1


def main():
    input = sys.stdin.read()
    pairs = [[literal_eval(y) for y in x.splitlines()] for x in input.split("\n\n")]

    correct = [i + 1 for i, (l, r) in enumerate(pairs) if compare(l, r) == -1]
    print("Part 1:", sum(correct))

    all_pairs = [lst for pair in pairs for lst in pair] + [[[2]], [[6]]]
    all_pairs.sort(key=cmp_to_key(compare))
    div1 = all_pairs.index([[2]]) + 1
    div2 = all_pairs.index([[6]]) + 1
    print("Part 2:", div1 * div2)


if __name__ == "__main__":
    main()
