# 59. Spiral Matrix II

[LeetCode Problem](https://leetcode.com/problems/spiral-matrix-ii/)

## Problem

Given a positive integer `n`, generate an `n x n` matrix filled with
the values `1` to `n^2` in spiral order.

```
Input:  n = 3
Output: [[1,2,3],[8,9,4],[7,6,5]]

Input:  n = 1
Output: [[1]]
```

**Constraints**
- `1 <= n <= 20`

This is the "write" counterpart to [Spiral Matrix
(54)](../54-spiral-matrix/) — instead of reading existing values off a
matrix in spiral order, values `1..n²` get written into a fresh
matrix in that same order. Both approaches mirror problem 54's two
solutions almost exactly.

## Approaches

### 1. Shrinking boundaries — `generateMatrix()`

Track four boundaries — `top`, `bottom`, `left`, `right` — delimiting
the still-unfilled square. Repeatedly:

1. Fill left → right along `top`, then push `top` down.
2. Fill top → bottom along `right`, then pull `right` in.
3. **If a row still remains**, fill right → left along `bottom`, then
   pull `bottom` up.
4. **If a column still remains**, fill bottom → top along `left`,
   then push `left` in.

A single counter, incremented after every write, supplies the next
value to place. Since the matrix here is always square, the "if a
row/column remains" guards only ever come into play on the very
innermost single-cell layer, but they're kept in for consistency with
the general pattern (and because the exact same code handles any
square size without special-casing).

- **Time:** `O(n²)` — every cell is written exactly once.
- **Space:** `O(1)` extra, not counting the output matrix itself.

### 2. Direct simulation with turn-on-obstacle — `generateMatrixSimulation()`

Walk the grid one cell at a time in a current direction (right, down,
left, up — cycling in that order), writing the next value into each
cell as it's visited. Whenever the next step would leave the grid or
land on an already-filled cell, turn 90 degrees clockwise instead.
Stop once every cell has a value.

Rather than a separate `visited` grid, this approach reuses the
matrix's own contents: an unfilled cell is still `0`, so checking
"has this cell already been written" is just checking for a nonzero
value — no extra memory needed beyond the output itself.

- **Time:** `O(n²)` — every cell is visited exactly once.
- **Space:** `O(1)` extra, since the matrix doubles as its own
  visited-tracker.

## Testing

`solution.py` runs both approaches against `n = 1, 2, 3, 4, 5`,
checking that:

- the matrix contains exactly the values `1` through `n²` (nothing
  missing or duplicated), and
- the matrix matches the expected spiral layout exactly.

```
python3 solution.py
```

All test cases pass for both implementations.