# 10. Regular Expression Matching

LeetCode: https://leetcode.com/problems/regular-expression-matching/
**Difficulty:** Hard

## Problem

Given an input string `s` and a pattern `p`, implement regular expression
matching with support for `.` and `*` where:

- `.` Matches any single character.
- `*` Matches zero or more of the preceding element.

The matching should cover the **entire** input string (not partial).

### Examples

| s | p | Output | Explanation |
|---|---|---|---|
| `"aa"` | `"a"` | `false` | `"a"` doesn't cover the whole string `"aa"` |
| `"aa"` | `"a*"` | `true` | `a*` repeats `'a'` once to make `"aa"` |
| `"ab"` | `".*"` | `true` | `.*` means zero or more of any character |

### Constraints

- `1 <= s.length <= 20`
- `1 <= p.length <= 30`
- `s` contains only lowercase English letters.
- `p` contains only lowercase English letters, `.`, and `*`.
- Every `*` in `p` is guaranteed to have a valid preceding character.

## Approach

`solution.py` implements two equivalent solutions, both based on the same
recurrence.

### Core idea

Let `dp(i, j)` mean "does `s[i:]` match `p[j:]`?" We want `dp(0, 0)`.

- If `p[j]` is followed by `*`, we have two choices:
  - **Skip** the `"char*"` pair entirely (treat it as zero occurrences):
    `dp(i, j+2)`
  - **Use** it, if the current characters match (`p[j] == s[i]` or
    `p[j] == '.'`): consume one character of `s` and stay at the same
    pattern position, since `*` can repeat: `dp(i+1, j)`
- Otherwise, it's a plain one-to-one match: `p[j]` must match `s[i]` (or be
  `.`), and we advance both: `dp(i+1, j+1)`
- Base case: an empty pattern only matches an empty string.

### 1. `isMatch` — bottom-up DP (table)

Builds a 2D table `dp[i][j]` for all suffixes of `s` and `p`, filled in
from the end of both strings backward (since `*` looks ahead in the
pattern, working backward means "ahead" is already computed).

**Time:** O(len(s) × len(p))
**Space:** O(len(s) × len(p))

### 2. `isMatchRecursive` — top-down memoized recursion

Same recurrence, expressed as a recursive function cached with
`functools.lru_cache`. Often easier to read since it mirrors the
recurrence directly, at the cost of recursion overhead.

**Time:** O(len(s) × len(p))
**Space:** O(len(s) × len(p)) (cache) + O(len(s) + len(p)) (call stack)

## Running

```bash
python3 solution.py
```

Runs a built-in test suite covering basic matches, `*` with zero
repetitions, `.*` wildcards, empty strings/patterns, and multi-`*`
patterns, printing pass/fail status for each case.