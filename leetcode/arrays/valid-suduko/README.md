# 36. Valid Sudoku

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/valid-sudoku/
**Topics:** Array, Hash Table, Matrix

## Problem

Determine if a `9 x 9` Sudoku board is valid. Only the **filled**
cells need to be validated according to the following rules:

1. Each **row** must contain the digits `1-9` without repetition.
2. Each **column** must contain the digits `1-9` without repetition.
3. Each of the nine `3 x 3` **sub-boxes** must contain the digits
   `1-9` without repetition.

> **Note:** A Sudoku board (partially filled) could be valid but not
> necessarily solvable. Only the filled cells need to be validated
> according to the rules above.

### Example

```
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
```

### Constraints

- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit `1-9` or `'.'`.

## Approach 1: Brute Force (Re-scan Per Rule)

Check each of the three rules with its own full pass over the board:

- For every row, collect its non-`'.'` digits into a list and check for
  duplicates by comparing the list's length against the length of the
  set built from it.
- Repeat the same check for every column.
- Repeat again for every `3 x 3` box.

This validates the board correctly, but revisits cells multiple times
(once per rule) instead of checking everything about a cell in one
pass.

- **Time:** `O(n^2)` for an `n x n` board (still linear in cell count,
  just with a higher constant from three separate full passes).
- **Space:** `O(n)` per row/column/box check for the temporary
  list/set.

## Approach 2: Single Pass with Hash Sets (Optimal)

Visit every cell exactly once. Maintain three arrays of sets:

- `rows[9]` — one set per row.
- `cols[9]` — one set per column.
- `boxes[9]` — one set per `3 x 3` box, indexed by
  `(r // 3) * 3 + (c // 3)`, which maps each cell's row/column to one
  of the nine boxes (numbered `0-8` in reading order).

For each filled cell `(r, c)` with digit `d`:

- If `d` is already in `rows[r]`, `cols[c]`, or `boxes[box_idx]`, the
  board is invalid — return `False` immediately.
- Otherwise, add `d` to all three sets and move on.

Every cell is checked against all three rules simultaneously in a
single visit, with `O(1)` set lookups and inserts.

- **Time:** `O(n^2)` for an `n x n` board (81 cells for standard
  Sudoku), each visited exactly once.
- **Space:** `O(n^2)` — 9 rows + 9 columns + 9 boxes, each holding up
  to 9 digits.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases using
  the classic LeetCode example board, a version with a duplicate in a
  column, a version with a duplicate inside a single box, and a
  completely empty (trivially valid) board.

## Complexity Summary

| Approach                          | Time   | Space |
|--------------------------------------|--------|-------|
| Brute Force (re-scan per rule)       | O(n^2) | O(n)  |
| Single Pass with Hash Sets (optimal) | O(n^2) | O(n^2) |