import sys
from io import StringIO


def read_input():
    instructions = []
    for line in sys.stdin:
        args = line.strip().split()
        if len(args) == 1:
            instructions.append((args[0], None))
        else:
            instructions.append((args[0], int(args[1])))
    return instructions


def print_crt(out, X, cycle):
    pos = (cycle - 1) % 40
    if pos == 0:
        out.write("\n")

    px = "█" if pos in [X - 1, X, X + 1] else " "
    out.write(px)


def update_cycle(cycle, strength, X):
    cycle += 1
    if (cycle - 20) % 40 == 0:
        strength += cycle * X
    return cycle, strength


def main():
    instructions = read_input()
    cycle = 1
    X = 1

    strength = 0
    out = StringIO()

    for instr, arg in instructions:
        print_crt(out, X, cycle)
        if instr == "addx":
            cycle, strength = update_cycle(cycle, strength, X)
            print_crt(out, X, cycle)
            X += arg
        cycle, strength = update_cycle(cycle, strength, X)

    print("Part 1", strength)
    print("Part 2", out.getvalue())


if __name__ == "__main__":
    main()
