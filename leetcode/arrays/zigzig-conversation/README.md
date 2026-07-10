# 6. Zigzag Conversion

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/zigzag-conversion/

## Problem

The string `"PAYPALISHIRING"` is written in a zigzag pattern on a given
number of rows like this:

```
P   A   H   N
A P L S I I G
Y   I   R
```

And then read line by line: `"PAHNAPLSIIGYIR"`.

Write the code that will take a string and make this conversion given a
number of rows:

```
string convert(string s, int numRows);
```

### Example 1
```
Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
```

### Example 2
```
Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:
P     I    N
A   L S  I G
Y A   H R
P     I
```

### Example 3
```
Input: s = "A", numRows = 1
Output: "A"
```

### Constraints
- `1 <= s.length <= 1000`
- `s` consists of English letters (lower-case and upper-case), `,` and `.`.
- `1 <= numRows <= 1000`

## Approach: Row Simulation

Rather than building a full 2D grid, we notice that as we scan the string
left to right, each character belongs to exactly one row, and the row index
follows a predictable "bounce" pattern:

```
row: 0, 1, 2, ..., numRows - 1, numRows - 2, ..., 1, 0, 1, 2, ...
```

So we can simulate the zigzag with a single pass:

1. Create one string buffer per row (`numRows` buffers total).
2. Track the `current_row` we're placing characters into and a
   `going_down` direction flag.
3. For each character in `s`, append it to `rows[current_row]`.
4. Whenever `current_row` hits the top (`0`) or bottom (`numRows - 1`), flip
   `going_down`.
5. Move `current_row` up or down based on the direction flag.
6. After processing every character, concatenate the row buffers in order
   to produce the final zigzagged string.

### Edge Case
If `numRows == 1` (or `numRows >= len(s)`), there's no zigzagging to do —
the original string is returned as-is.

## Complexity

| | Complexity |
|---|---|
| Time | `O(n)` — each character is processed exactly once. |
| Space | `O(n)` — the row buffers collectively hold every character once (output space is not counted against extra space in some conventions, but is included here for completeness). |

## Alternative Approaches

- **Mathematical / Index Jumping** — directly compute, for each row, the
  indices of `s` that belong to it using the cycle length
  `2 * numRows - 2`, then build the output row by row without buffers.
  Same `O(n)` time, but can be done with `O(1)` extra space (excluding the
  output).

## Files

- [`solution.py`](./solution.py) — Python solution using the row simulation
  approach.