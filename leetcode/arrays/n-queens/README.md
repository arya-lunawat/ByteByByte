# 51. N-Queens

[LeetCode Problem](https://leetcode.com/problems/n-queens/)

## Problem

The n-queens puzzle is the problem of placing `n` queens on an
`n x n` chessboard so that no two queens attack each other. Given an
integer `n`, return **all** distinct solutions, in any order. Each
solution is a board configuration as a list of strings, with `'Q'`
for a queen and `'.'` for an empty square.

```
Input:  n = 4
Output: [[".Q..","...Q","Q...","..Q."],
          ["..Q.","Q...","...Q",".Q.."]]

Input:  n = 1
Output: [["Q"]]
```

**Constraints**
- `1 <= n <= 9`

## Approaches

Both approaches share the same key insight: since no two queens can
ever occupy the same row, a solution is really just a decision, for
each row, of *which single column* to place its queen in. That turns
the search into "try every column for row 0, then row 1, then ...",
backtracking whenever a column conflicts with an already-placed
queen. They differ only in how attacks are tracked.

### 1. Backtracking with three tracking sets — `solveNQueens()`

A queen at `(row, col)` attacks another queen at `(row2, col2)` if
they share a column, or a diagonal. The two diagonal directions have
a simple invariant:

- `row + col` is constant along every "`/`" diagonal
- `row - col` is constant along every "`\`" diagonal

So three plain sets — `cols`, `diag1` (`row + col` values in use),
and `diag2` (`row - col` values in use) — let every safety check and
update happen in `O(1)`, without rescanning previously placed queens.

- **Time:** `O(n!)` — the number of columns still available shrinks
  by roughly one per row as columns/diagonals fill up, matching the
  classic n-queens search-space bound.
- **Space:** `O(n²)` for the collected boards, `O(n)` for the
  recursion stack and the three tracking sets.

### 2. Backtracking with bitmask tracking — `solveNQueensBitmask()`

Identical row-by-row search, but each of "columns attacked", "'/'
diagonals attacked", and "'\' diagonals attacked" is packed into a
single integer bitmask instead of a Python `set`. At each row:

```
available = full_mask & ~(cols | diag1 | diag2)
```

gives every column that's free in all three dimensions at once, and
the classic `available & -available` trick pulls out the lowest set
bit — the next column to try — without looping over every column
index to check it individually.

- **Time:** `O(n!)` — same search space as approach 1.
- **Space:** `O(n²)` for the collected boards, `O(n)` for the
  recursion stack and per-row bitmasks.

Same asymptotic complexity as approach 1, but bitwise operations are
typically noticeably faster than set operations in practice, which
matters once `n` gets close to 9.

## Testing

`solution.py` runs both approaches against every `n` from 1 to 9 and
checks the result against the known solution counts for the n-queens
problem (1, 0, 0, 2, 10, 4, 40, 92, 352). For every returned board, a
helper independently re-verifies that no two queens share a row,
column, or diagonal — and for `n = 1` and `n = 4`, the boards are also
compared exactly (order-independent) against the boards given in the
problem statement.

```
python3 solution.py
```

All test cases pass for both implementations.