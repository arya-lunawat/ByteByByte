# 20. Valid Parentheses

LeetCode: https://leetcode.com/problems/valid-parentheses/
**Difficulty:** Easy

## Problem

Given a string `s` containing just the characters `(`, `)`, `{`, `}`,
`[`, `]`, determine if the input string is valid. A string is valid if:

1. Open brackets are closed by the same type of bracket.
2. Open brackets are closed in the correct order.
3. Every closing bracket has a matching, still-open bracket of the same
   type.

### Examples

| s | Output | Explanation |
|---|---|---|
| `"()"` | `true` | Simple matched pair |
| `"()[]{}"` | `true` | Three separate matched pairs |
| `"(]"` | `false` | Mismatched bracket types |
| `"([)]"` | `false` | Wrong closing order |

### Constraints

- `1 <= s.length <= 10^4`
- `s` consists only of `()[]{}`

## Approach

`solution.py` implements two solutions.

### 1. `isValid` — stack (primary)

This is the textbook use case for a stack: brackets need to close in
**last-opened, first-closed** order, which is exactly what a stack gives
you.

- Walk through the string one character at a time.
- If it's an **opening** bracket, push it onto the stack.
- If it's a **closing** bracket, it must match whatever is currently on
  top of the stack (the most recent unclosed bracket). If the stack is
  empty (nothing to close) or the top doesn't match the expected opening
  bracket, the string is immediately invalid. Otherwise, pop the matched
  opening bracket off.
- At the end, the string is valid only if the stack is completely empty —
  if anything's left, it means some opening bracket was never closed.

**Time:** O(n) — single pass over the string.
**Space:** O(n) — worst case (e.g. all opening brackets) the stack holds
every character.

### 2. `isValidReplace` — repeated substring removal (for comparison)

Repeatedly strip out any innermost matched pair (`"()"`, `"[]"`, `"{}"`)
from the string until no more removals happen. If the string reduces all
the way down to empty, it was valid. Conceptually simple, but each
`replace` call is a fresh O(n) scan, and it may take up to `n/2` rounds —
much less efficient than the stack approach, and included mainly to
cross-check correctness in the test suite.

**Time:** O(n²) — up to n/2 removal passes, each scanning/rebuilding an
O(n) string.
**Space:** O(n) — new strings created on each replacement.

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (covering matched pairs, mismatched types,
wrong nesting order, unclosed/unopened brackets, an empty string, and
deeply nested brackets), comparing both solutions and printing pass/fail
for each case.