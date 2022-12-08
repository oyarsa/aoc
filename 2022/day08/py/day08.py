import sys

import numpy as np

matrix = np.array([[int(x) for x in line] for line in sys.stdin.read().splitlines()])
m, n = matrix.shape

counter = 0
for i in range(m):
    for j in range(n):
        height = matrix[i, j]
        # check row
        row_l = all(matrix[i, a] < height for a in range(j))
        row_r = all(matrix[i, a] < height for a in range(j + 1, n))
        # check column
        col_u = all(matrix[a, j] < height for a in range(i))
        col_d = all(matrix[a, j] < height for a in range(i + 1, m))

        if row_l or row_r or col_u or col_d:
            counter += 1

print("Part 1", counter)

max_score = 0
for i in range(m):
    for j in range(n):
        height = matrix[i, j]
        left, right, up, down = 0, 0, 0, 0

        for a in range(j - 1, -1, -1):
            left += 1
            if matrix[i, a] >= height:
                break

        for a in range(j + 1, n):
            right += 1
            if matrix[i, a] >= height:
                break

        for a in range(i - 1, -1, -1):
            up += 1
            if matrix[a, j] >= height:
                break

        for a in range(i + 1, m):
            down += 1
            if matrix[a, j] >= height:
                break

        score = left * right * up * down
        max_score = max(score, max_score)

print("Part 2", max_score)
