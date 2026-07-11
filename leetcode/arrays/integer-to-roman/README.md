# 12. Integer to Roman

LeetCode: https://leetcode.com/problems/integer-to-roman/
**Difficulty:** Medium

## Problem

Roman numerals are represented by seven symbols:

| Symbol | Value |
|---|---|
| I | 1 |
| V | 5 |
| X | 10 |
| L | 50 |
| C | 100 |
| D | 500 |
| M | 1000 |

Numerals are built by placing symbols from highest to lowest value, with
special "subtractive" pairs for 4 and 9 in each place value (`IV`=4,
`IX`=9, `XL`=40, `XC`=90, `CD`=400, `CM`=900).

Given an integer, convert it to its Roman numeral representation.

### Examples

| num | Output | Explanation |
|---|---|---|
| `3749` | `"MMMDCCXLIX"` | 3000=MMM, 700=DCC, 40=XL, 9=IX |
| `58` | `"LVIII"` | 50=L, 8=VIII |
| `1994` | `"MCMXCIV"` | 1000=M, 900=CM, 90=XC, 4=IV |

### Constraints

- `1 <= num <= 3999`

## Approach

`solution.py` implements two solutions.

### 1. `intToRoman` — greedy subtraction (primary)

Use a table of `(value, symbol)` pairs ordered from largest to smallest,
where the subtractive forms (`900, "CM"`, `40, "XL"`, etc.) are included
as first-class entries alongside the standard ones. For each entry,
figure out how many times that value divides into what's left of `num`
(via `divmod`), append that many copies of the symbol, and move on.
Because the table already encodes the subtractive cases, no special-casing
is needed — the same loop handles `4`, `40`, `400`, `9`, `90`, `900` the
same way it handles `1`, `10`, `100`, `1000`.

**Time:** O(1) — the table has a fixed 13 entries and `num` is bounded by
3999, so the loop count is constant regardless of input size.
**Space:** O(1) — fixed-size table; output length is bounded (max 15
characters, e.g. `3888` → `"MMMDCCCLXXXVIII"`).

### 2. `intToRomanDigitByDigit` — precomputed digit tables (for comparison)

Since `num <= 3999`, it has at most 4 decimal digits (thousands,
hundreds, tens, ones). Each place value only ever needs one of 10 possible
Roman fragments (e.g. hundreds digit `7` → `"DCC"`), so we can precompute
a lookup table of size 10 for each place and just index into it directly —
no loop, no arithmetic beyond splitting `num` into digits.

**Time:** O(1) — always exactly 4 table lookups
**Space:** O(1) — fixed-size lookup tables

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (covering all six subtractive cases, the
problem's own examples, and the boundary value `3999`), comparing both
solutions and printing pass/fail for each case.