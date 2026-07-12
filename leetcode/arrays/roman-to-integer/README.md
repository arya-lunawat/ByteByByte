# 13. Roman to Integer

LeetCode: https://leetcode.com/problems/roman-to-integer/description/
**Difficulty:** Easy

## Problem

Roman numerals use seven symbols:

| Symbol | Value |
|---|---|
| I | 1 |
| V | 5 |
| X | 10 |
| L | 50 |
| C | 100 |
| D | 500 |
| M | 1000 |

Usually written largest-to-smallest (e.g. `"XXVII"` = 27), but six cases
use a subtractive form: `IV`=4, `IX`=9, `XL`=40, `XC`=90, `CD`=400,
`CM`=900.

Given a valid Roman numeral, convert it to an integer.

### Examples

| s | Output | Explanation |
|---|---|---|
| `"III"` | `3` | I+I+I |
| `"LVIII"` | `58` | L=50, V=5, III=3 |
| `"MCMXCIV"` | `1994` | M=1000, CM=900, XC=90, IV=4 |

### Constraints

- `1 <= s.length <= 15`
- `s` contains only `I, V, X, L, C, D, M`
- `s` is guaranteed to be a valid Roman numeral in `[1, 3999]`

## Approach

`solution.py` implements two solutions.

### 1. `romanToInt` — single left-to-right scan (primary)

The trick: in a subtractive pair like `"IV"`, the smaller-valued symbol
always comes *immediately before* a strictly larger one. So rather than
special-casing the six subtractive pairs, just look one symbol ahead at
each position:

- If the current symbol's value is **less than** the next symbol's value,
  we're at the start of a subtractive pair — subtract the current value.
- Otherwise, add it normally.

This naturally falls out of the numeral's structure — `"IV"` becomes
`-1 + 5 = 4`, `"IX"` becomes `-1 + 10 = 9`, and so on — with no explicit
pair-detection logic needed.

**Time:** O(n) — one pass over the string
**Space:** O(1) — fixed 7-entry lookup table

### 2. `romanToIntReplace` — pair substitution (for comparison)

Replaces each of the six known subtractive pairs (`"IV"`, `"IX"`, `"XL"`,
`"XC"`, `"CD"`, `"CM"`) with an equivalent run of plain-additive symbols
(e.g. `"IV"` → `"IIII"`), then just sums every character's value. Simple
to reason about, but does extra work building intermediate strings.

**Time:** O(n) — six fixed replacements plus a final summation pass
**Space:** O(n) — string replacement creates new strings

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (covering all six subtractive pairs, the
problem's own examples, a single-symbol input, and the boundary value
`3999`), comparing both solutions and printing pass/fail for each case.