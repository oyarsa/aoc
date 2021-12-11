def gauss(x, y):
    n = abs(x - y) + 1
    return (n * (n - 1)) // 2


prob = [int(x) for x in input().split(",")]
ans = min(sum(abs(x - y) for y in prob) for x in range(min(prob), max(prob) + 1))
print("Part 1:", ans)
ans = min(sum(gauss(x, y) for y in prob) for x in range(min(prob), max(prob) + 1))
print("Part 2:", ans)
