# 62. Unique Paths

[LeetCode Problem](https://leetcode.com/problems/unique-paths/)

## Problem

A robot starts at the top-left corner of an `m x n` grid and can only
move down or right. Return the number of distinct paths to the
bottom-right corner.

```
Input:  m = 3, n = 7
Output: 28

Input:  m = 3, n = 2
Output: 3
Explanation: Right->Down->Down, Down->Down->Right, Down->Right->Down.
```

**Constraints**
- `1 <= m, n <= 100`

## Approaches

### 1. Dynamic programming with a rolling row — `uniquePaths()`

Let `dp[j]` be the number of unique paths to reach column `j` of the
*current* row. Any cell can only be reached by moving down (from the
cell above) or right (from the cell to the left), so:

```
dp[j] = dp[j] (from the row above, not yet overwritten this pass)
      + dp[j - 1] (from the same row, already updated this pass)
```

The first row is initialized to all `1`s — there's only one way to
reach any cell in the top row (move right repeatedly). Then the same
array is updated in place, row by row, left to right: at the moment
`dp[j]` is read, it still holds the value from the row above (not yet
overwritten), while `dp[j-1]` has already been updated for the
current row — exactly the two values the recurrence needs.

- **Time:** `O(m · n)` — one addition per grid cell.
- **Space:** `O(n)` — a single rolling row, instead of a full
  `O(m · n)` 2D table.

### 2. Direct combinatorics — `uniquePathsCombinatorics()`

Every path from corner to corner consists of exactly `(m - 1)` "down"
moves and `(n - 1)` "right" moves, in some order — `(m - 1) + (n - 1)`
moves total. The number of distinct orderings is exactly the number
of ways to choose which of those move-slots are "down" moves:

```
C(m + n - 2, m - 1)
```

`math.comb` computes this directly and exactly (as an arbitrary
precision integer, no floating-point rounding).

- **Time:** effectively `O(min(m, n))` — `math.comb`'s internal
  computation is roughly linear in the smaller chosen value.
- **Space:** `O(1)` — no table at all.

This is dramatically faster than the DP approach and is the natural
solution once the "count paths on a grid" framing is recognized as a
combinations-counting problem in disguise.

## Testing

`solution.py` runs both approaches against 10 test cases, including
the problem's own examples, `1×1` and `1×n`/`n×1` degenerate grids
(exactly one path), a square grid, and the maximum-size `100×100`
grid — whose exact answer (a 62-digit integer) is verified precisely,
confirming `math.comb` avoids any floating-point precision loss.

```
python3 solution.py
```

All test cases pass for both implementations.