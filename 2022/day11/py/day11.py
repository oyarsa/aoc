import copy
import math
import re
import sys
from dataclasses import dataclass
from math import floor

lines = sys.stdin.read()


@dataclass
class Monkey:
    idx: int
    items: list[int]
    operation: tuple[str, int]  # (op, value)
    test: tuple[int, int, int]  # (divisible by, true, false)

    def __str__(self):
        return (
            f"Monkey {self.idx}:\n"
            f"  Starting items: {', '.join(str(x) for x in self.items)}\n"
            f"  Operation: new = old {self.operation[0]} {self.operation[1]}\n"
            f"  Test: divisible by {self.test[0]}\n"
            f"    If true: throw to monkey {self.test[1]}\n"
            f"    If false: throw to monkey {self.test[2]}\n"
        )


def read_input():
    monkeys: list[Monkey] = []
    for monkey in lines.split("\n\n"):
        entries = monkey.splitlines()

        idx_match = re.match(r"Monkey (\d+):", entries[0])
        assert idx_match is not None, entries[0]
        i = int(idx_match.group(1))

        starting_match = re.match(r".*Starting items: (.+)", entries[1])
        assert starting_match is not None, entries[1]
        starting_items = [int(x) for x in starting_match.group(1).split(", ")]

        operation_match = re.match(r".*Operation: new = old (\+|\*) (.+)", entries[2])
        assert operation_match is not None, entries[2]
        value = operation_match.group(2)
        if value == "old":
            value = -1
        else:
            value = int(value)
        operation = (operation_match.group(1), value)

        divisble_match = re.match(r".*Test: divisible by (\d+)", entries[3])
        assert divisble_match is not None, entries[3]
        divisble = int(divisble_match.group(1))

        test_true_match = re.match(r".*If true: throw to monkey (\d+)", entries[4])
        assert test_true_match is not None, entries[4]
        test_true = int(test_true_match.group(1))

        test_false_match = re.match(r".*If false: throw to monkey (\d+)", entries[5])
        assert test_false_match is not None, entries[5]
        test_false = int(test_false_match.group(1))

        monkey = Monkey(
            i,
            starting_items,
            operation,
            (divisble, test_true, test_false),
        )
        monkeys.append(monkey)
    return monkeys


def solve(monkeys, n_rounds, transform):
    monkey_inspections = [0] * len(monkeys)
    for _ in range(n_rounds):
        for monkey in monkeys:
            while monkey.items:
                monkey_inspections[monkey.idx] += 1
                item = monkey.items.pop(0)

                op, val = monkey.operation
                if op == "+":
                    new_item = item + val
                elif op == "*":
                    if val == -1:
                        new_item = item**2
                    else:
                        new_item = item * val
                else:
                    raise ValueError(f"Unknown operation {monkey.operation[0]}")

                new_item = transform(new_item)

                number, tgt_true, tgt_false = monkey.test
                if new_item % number == 0:
                    monkeys[tgt_true].items.append(new_item)
                else:
                    monkeys[tgt_false].items.append(new_item)

    top1, top2 = sorted(monkey_inspections, reverse=True)[:2]
    return top1 * top2


monkeys = read_input()
lcm = math.lcm(*(m.test[0] for m in monkeys))
print("Part 1", solve(copy.deepcopy(monkeys), 20, lambda x: floor(x / 3)))
print("Part 2", solve(monkeys, 10_000, lambda x: x % lcm))
