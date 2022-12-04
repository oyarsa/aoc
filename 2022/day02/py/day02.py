import sys

scores = {
    "X": 1,
    "Y": 2,
    "Z": 3,
    "w": 6,
    "d": 3,
    "l": 0,
}

plays: dict[tuple[str, str], str] = {
    ("X", "A"): "d",
    ("X", "B"): "l",
    ("X", "C"): "w",
    ("Y", "A"): "w",
    ("Y", "B"): "d",
    ("Y", "C"): "l",
    ("Z", "A"): "l",
    ("Z", "B"): "w",
    ("Z", "C"): "d",
}


rounds = [line.split() for line in sys.stdin]

total = 0
for theirs, mine in rounds:
    result = scores[plays[(mine, theirs)]]
    move = scores[mine]
    total += result + move

print("Part 1", total)

new_plays: dict[tuple[str, str], str] = {
    (theirs, result): mine for (mine, theirs), result in plays.items()
}

total2 = 0
move_map = {
    'X': 'l',
    'Y': 'd',
    'Z': 'w'
}
for theirs, result in rounds:
    mine = new_plays[(theirs, move_map[result])]
    total2 += scores[mine] + scores[move_map[result]]

print("Part 2", total2)
