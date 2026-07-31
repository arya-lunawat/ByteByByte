# 52. N-Queens II

[LeetCode Problem](https://leetcode.com/problems/n-queens-ii/)

## Problem

The n-queens puzzle is the problem of placing `n` queens on an
`n x n` chessboard so that no two queens attack each other. Given an
integer `n`, return the **number** of distinct solutions to the
n-queens puzzle.

```
Input:  n = 4
Output: 2
Explanation: There are two distinct solutions to the 4-queens puzzle.

Input:  n = 1
Output: 1
```

**Constraints**
- `1 <= n <= 9`

This is the "count only" sibling of
[N-Queens (51)](../51-n-queens/): the search is identical, but since
the actual board layouts are never needed, there's no reason to pay
the `O(n²)` cost of building a board string for every solution — just
increment a counter.

## Approaches

Both approaches reuse the same core insight as problem 51: since no
two queens can ever share a row, the search reduces to choosing, one
row at a time, which single column that row's queen goes in,
backtracking on conflicts. They differ only in how "column/diagonal
under attack" is tracked.

### 1. Backtracking with three tracking sets — `totalNQueens()`

A queen at `(row, col)` conflicts with another at `(row2, col2)` if
they share a column or a diagonal. The two diagonal directions have a
simple invariant: `row + col` is constant along every "`/`" diagonal,
and `row - col` is constant along every "`\`" diagonal. Three sets —
`cols`, `diag1`, `diag2` — let every safety check and update happen in
`O(1)`. When a row index reaches `n`, that's one complete, valid
placement — the counter increments and the function returns, with no
board ever constructed.

- **Time:** `O(n!)` — the standard n-queens search-space bound; the
  number of still-available columns shrinks by roughly one per row.
- **Space:** `O(n)` for the recursion stack and the three tracking
  sets — no `O(n²)` boards to store, unlike problem 51.

### 2. Backtracking with bitmask tracking — `totalNQueensBitmask()`

Same row-by-row search, but "columns attacked", "'/' diagonals
attacked", and "'\' diagonals attacked" are each packed into a single
integer bitmask. At each row,
`available = full_mask & ~(cols | diag1 | diag2)` gives every free
column across all three dimensions at once, and the bit trick
`available & -available` extracts the next column to try without
looping over each index individually.

- **Time:** `O(n!)` — same search space as approach 1.
- **Space:** `O(n)` for the recursion stack and per-call bitmasks.

Same asymptotic complexity as approach 1, but bitwise operations tend
to be noticeably faster in practice than the equivalent set
operations, especially as `n` approaches 9.

## Testing

`solution.py` runs both approaches against every `n` from 1 to 9 and
checks the returned count against the known n-queens solution counts
(1, 0, 0, 2, 10, 4, 40, 92, 352 respectively).

```
python3 solution.py
```

All test cases pass for both implementations.