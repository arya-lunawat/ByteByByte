# 48. Rotate Image

[LeetCode Problem](https://leetcode.com/problems/rotate-image/)

## Problem

Given an `n x n` 2D matrix representing an image, rotate the image by
90 degrees **clockwise**, **in-place** — the input matrix must be
modified directly; allocating a second 2D matrix isn't allowed.

```
Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output:          [[7,4,1],[8,5,2],[9,6,3]]
```

**Constraints**
- `n == matrix.length == matrix[i].length`
- `1 <= n <= 20`
- `-1000 <= matrix[i][j] <= 1000`

The in-place requirement is the whole challenge here — without it,
you'd just build a new matrix where `result[j][n-1-i] = matrix[i][j]`
and call it a day. Both approaches below use only `O(1)` extra space.

## Approaches

### 1. Transpose, then reverse each row — `rotate()`

A 90-degree clockwise rotation decomposes into two simpler in-place
steps:

1. **Transpose** the matrix across its main diagonal — swap
   `matrix[i][j]` with `matrix[j][i]` for every `i < j`.
2. **Reverse every row.**

After transposing, row `i` already holds the values that belong in
column `i` of the final result, just written top-to-bottom instead of
the bottom-to-top order the rotation needs — reversing each row
corrects that.

- **Time:** `O(n²)` — every cell is touched a constant number of times.
- **Space:** `O(1)` extra.

This is the standard, easiest-to-remember solution: two well-known
primitives (transpose, reverse) composed together.

### 2. Layer-by-layer 4-way cycle — `rotateLayerByLayer()`

Think of the matrix as concentric square rings ("layers"), from the
outermost ring inward. For each layer, walk along its top edge; for
every position, cycle the four cells that correspond to it —
top, right, bottom, left — one step clockwise, using a single temp
variable to avoid overwriting a value before it's been moved:

```
temp   <- top
top    <- left
left   <- bottom
bottom <- right
right  <- temp (the original top)
```

This does the identical rotation without leaning on transpose/reverse
as building blocks — it's the more "manual" version, useful for seeing
directly why each element ends up where it does.

- **Time:** `O(n²)` — every cell is moved exactly once.
- **Space:** `O(1)` extra — one temp variable per 4-cycle.

## Testing

`solution.py` runs both approaches against 8 test cases, covering
`1x1` up to `5x5` matrices, negative values, an all-zero matrix, and
the two examples from the problem statement. Each case checks that:

- the method returns `None` (per the in-place interface), and
- the mutated matrix exactly matches the expected rotated result.

```
python3 solution.py
```

All test cases pass for both implementations.