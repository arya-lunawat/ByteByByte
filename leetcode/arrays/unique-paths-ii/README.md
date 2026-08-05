# 63. Unique Paths II

[LeetCode Problem](https://leetcode.com/problems/unique-paths-ii/)

## Problem

A robot starts at the top-left corner of an `m x n` grid and can only
move down or right, trying to reach the bottom-right corner. Some
cells are obstacles (marked `1`) that the robot cannot enter (`0`
marks open space). Return the number of distinct obstacle-free paths.

```
Input:  obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
Explanation: One obstacle in the middle of a 3x3 grid; two paths remain:
  Right -> Right -> Down -> Down
  Down -> Down -> Right -> Right

Input:  obstacleGrid = [[0,1],[0,0]]
Output: 1
```

**Constraints**
- `m == obstacleGrid.length`
- `n == obstacleGrid[i].length`
- `1 <= m, n <= 100`
- `obstacleGrid[i][j]` is `0` or `1`.

This is the obstacle-aware extension of [Unique Paths
(62)](../62-unique-paths/): same "sum the ways in from above and from
the left" recurrence, plus one rule — a cell the robot can never stand
on contributes exactly zero paths.

## Approaches

### 1. Dynamic programming with a rolling row — `uniquePathsWithObstacles()`

Same `dp[j] = (ways from above) + (ways from the left)` recurrence as
the obstacle-free version, computed row by row with a single rolling
array. The one addition: whenever the current cell is an obstacle,
`dp[j]` is forced to `0`, overriding whatever it would otherwise sum
to. That single override is enough to correctly handle an obstacle
anywhere — including at the very start (making the whole answer `0`
immediately) or one that fully blocks an entire row or column
partway through.

- **Time:** `O(m · n)` — one check, and possibly one addition, per
  cell.
- **Space:** `O(n)` — a single rolling row instead of a full
  `O(m · n)` table.

### 2. Dynamic programming with a full 2D table — `uniquePathsWithObstacles2D()`

The more explicit version: build a full `rows x cols` table where
`dp[i][j]` holds the number of ways to reach `(i, j)`. An obstacle
cell is always `0`; otherwise `dp[i][j] = dp[i-1][j] + dp[i][j-1]`,
treating any out-of-bounds neighbor (the top row or the left column)
as contributing `0`. The start cell `dp[0][0]` is seeded to `1`
unless it's itself an obstacle.

- **Time:** `O(m · n)` — one computation per cell.
- **Space:** `O(m · n)` — the full 2D table.

Uses more memory than the rolling-row version, but keeps every
intermediate state visible — useful for debugging, or as a starting
point for variants that need to look back further than a single row.

## Testing

`solution.py` runs both approaches against 10 test cases, including
the problem's own examples, a single open cell, a single obstacle
cell (`[[1]]` → 0 paths), single-row and single-column grids, an
obstacle that fully blocks a row (0 paths), and a larger 4×4 grid with
multiple scattered obstacles.

```
python3 solution.py
```

All test cases pass for both implementations.