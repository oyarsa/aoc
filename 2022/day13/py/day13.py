import sys
from ast import literal_eval
from functools import cmp_to_key


def compare(left, right):
    match left, right:
        case int(l), int(r):
            return l - r
        case [], r:
            return -1
        case l, []:
            return 1
        case [], []:
            return 0
        case int(l), _:
            left = [l]
        case _, int(r):
            right = [r]

    if (r := compare(left[0], right[0])) != 0:
        return r
    return compare(left[1:], right[1:])


def main():
    input = sys.stdin.read()
    pairs = [[literal_eval(y) for y in x.splitlines()] for x in input.split("\n\n")]

    correct = sum(i + 1 for i, (l, r) in enumerate(pairs) if compare(l, r) < 0)
    print("Part 1:", correct)

    dividers = [[[2]], [[6]]]
    all_pairs = [lst for pair in pairs for lst in pair] + dividers
    all_pairs.sort(key=cmp_to_key(compare))
    div1, div2 = (all_pairs.index(div) for div in dividers)
    print("Part 2:", (div1 + 1) * (div2 + 1))


if __name__ == "__main__":
    main()
