# 22. Generate Parentheses

LeetCode: https://leetcode.com/problems/generate-parentheses/
**Difficulty:** Medium

## Problem

Given `n` pairs of parentheses, generate all combinations of
well-formed (balanced) parentheses.

### Examples

| n | Output |
|---|---|
| `3` | `["((()))","(()())","(())()","()(())","()()()"]` |
| `1` | `["()"]` |

### Constraints

- `1 <= n <= 8`

## Approach

`solution.py` implements two solutions.

### 1. `generateParenthesis` — backtracking with count constraints (primary)

Build each combination one character at a time, tracking how many
opening and closing parentheses have been placed so far (`open_count`,
`close_count`). At each step there are up to two valid moves:

- Add `'('` — allowed as long as `open_count < n` (we haven't used up all
  `n` opening parens yet).
- Add `')'` — allowed as long as `close_count < open_count` (closing here
  wouldn't create more `)` than `(` so far, which would make the prefix
  unbalanceable).

A combination is complete once its length reaches `2n`. Because every
move is only taken when it keeps the string a valid *prefix* of some
well-formed sequence, every completed string is automatically valid —
there's no need for a separate "is this balanced?" check afterward.

**Time:** O(4ⁿ / √n) — the number of valid combinations is the `n`-th
Catalan number, and building each one costs O(n), giving the classic
Catalan-number bound.
**Space:** O(n) for the recursion depth and current path (not counting
the output).

### 2. `generateParenthesisDP` — bottom-up dynamic programming (for comparison)

Every valid combination with `k` pairs can be decomposed as:

```
"(" + <valid combination with i pairs> + ")" + <valid combination with (k-1-i) pairs>
```

for some split point `i` from `0` to `k-1` — this mirrors how any
balanced sequence splits around its very first matching closing bracket.
`dp[k]` holds every valid combination using `k` pairs, built up from
`dp[0] = [""]` through `dp[n]`.

**Time:** O(4ⁿ / √n) — same Catalan-number bound, computed bottom-up.
**Space:** O(4ⁿ / √n) — stores full combination lists for every count
from `0` to `n` along the way, more than the backtracking version needs.

## Running

```bash
python3 solution.py
```

Runs a built-in test suite comparing both solutions against the
problem's own examples for `n = 1, 2, 3`, then cross-checks the *count*
of generated combinations against the closed-form Catalan number formula
`C(2n, n) / (n + 1)` for every `n` from 1 to 8 (the full allowed range),
printing pass/fail for each case.