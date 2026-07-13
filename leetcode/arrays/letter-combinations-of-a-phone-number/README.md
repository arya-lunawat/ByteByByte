# 17. Letter Combinations of a Phone Number

LeetCode: https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/
**Difficulty:** Medium

## Problem

Given a string containing digits from `2-9`, return all possible letter
combinations that the number could represent (like on an old telephone
keypad). Return the answer in any order.

```
2: "abc"    3: "def"    4: "ghi"    5: "jkl"
6: "mno"    7: "pqrs"   8: "tuv"    9: "wxyz"
```

`1` maps to no letters.

### Examples

| digits | Output |
|---|---|
| `"23"` | `["ad","ae","af","bd","be","bf","cd","ce","cf"]` |
| `""` | `[]` |
| `"2"` | `["a","b","c"]` |

### Constraints

- `0 <= digits.length <= 4`
- `digits[i]` is a digit in `['2', '9']`

## Approach

`solution.py` implements two solutions, both built around the same
lookup table (`DIGIT_TO_LETTERS`) mapping each digit to its letters.

### 1. `letterCombinations` — backtracking / DFS (primary)

Build combinations one digit position at a time using a `path` list as
the current partial combination:

- At each digit index, try every letter that digit could map to.
- Append the letter to `path` and recurse into the next digit.
- After returning from the recursive call, pop the letter off (backtrack)
  before trying the next letter — this reuses the same `path` list across
  all branches instead of allocating a new one each time.
- When the path's length equals the number of digits, it's a complete
  combination — join it into a string and add it to the results.

The empty-string input is handled as a special case up front, since the
problem defines the answer for `digits = ""` as an empty list (not a
single empty combination).

**Time:** O(4ⁿ × n) where n = `len(digits)` — up to 4 letters per digit
(digits `7` and `9` have 4 each), and each of the up-to-4ⁿ combinations
costs O(n) to assemble.
**Space:** O(n) for the recursion depth and current path (not counting
the output itself).

### 2. `letterCombinationsIterative` — layer-by-layer expansion (for comparison)

Starts with a list containing just `[""]`, then for each digit, expands
every existing partial combination by every letter that digit maps to —
essentially a breadth-first, list-comprehension version of the same
branching process, with no explicit recursion or backtracking.

**Time:** O(4ⁿ × n) — same bound as backtracking.
**Space:** O(4ⁿ × n) — keeps a full list of all combinations built so far
at each step, rather than just one path at a time.

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (covering the problem's own examples, the
empty-string case, a single 4-letter digit, and a two 4-letter-digit
combination), comparing the backtracking and iterative results and
printing pass/fail for each case.