# 64. Minimum Path Sum

[LeetCode Problem](https://leetcode.com/problems/minimum-path-sum/)

## Problem

Given an `m x n` grid of non-negative numbers, find a path from the
top-left to the bottom-right corner that minimizes the sum of all
numbers along it. Movement is restricted to down or right only.

```
Input:  grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: The path 1 -> 3 -> 1 -> 1 -> 1 minimizes the sum.

Input:  grid = [[1,2,3],[4,5,6]]
Output: 12
```

**Constraints**
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 200`
- `0 <= grid[i][j] <= 200`

This is the "minimize the sum" cousin of [Unique Paths
(62)](../62-unique-paths/) and [Unique Paths II
(63)](../63-unique-paths-ii/) — same down-or-right movement rule, but
tracking the cheapest cost to reach each cell instead of the number of
ways to reach it.

## Approaches

### 1. In-place DP on the input grid — `minPathSum()`

The cheapest path to any cell `(i, j)` is that cell's own value plus
whichever of "cheapest path to the cell above" or "cheapest path to
the cell to the left" is smaller:

```
grid[i][j] += min(grid[i-1][j], grid[i][j-1])
```

The first row can only be reached by moving right repeatedly, so each
of its cells just accumulates the running sum from its left neighbor;
the first column similarly only accumulates from above. Updating the
grid in place, row by row and left to right, guarantees
`grid[i-1][j]` and `grid[i][j-1]` are already finalized by the time
`(i, j)` is processed.

- **Time:** `O(m · n)` — one comparison and addition per cell.
- **Space:** `O(1)` extra — reuses the input grid instead of
  allocating a separate table.

**Mutates the input grid** — use approach 2 if the caller needs the
original grid preserved.

### 2. Rolling 1D row, input left untouched — `minPathSumRollingRow()`

Identical recurrence, but computed into a separate reusable row `dp`
instead of overwriting the caller's grid. For each row:

- `dp[0]` accumulates straight down the first column.
- Every other `dp[j]` becomes `grid[i][j] + min(dp[j], dp[j-1])`,
  where `dp[j]` (not yet overwritten this pass) still holds the value
  from the row above, and `dp[j-1]` has already been updated for the
  current row — exactly the two values the recurrence needs.

- **Time:** `O(m · n)` — one comparison and addition per cell.
- **Space:** `O(n)` — one rolling row.

Worth using whenever the input grid must stay unmodified for the
caller, at the cost of one extra array of length `n`.

## Testing

`solution.py` runs both approaches against 10 test cases, including
the problem's own examples, `1x1` grids, single-row and
single-column grids, an all-zero grid, and two larger grids whose
correct minimum was independently confirmed with an exhaustive
brute-force search over every down/right path.

```
python3 solution.py
```

All test cases pass for both implementations.