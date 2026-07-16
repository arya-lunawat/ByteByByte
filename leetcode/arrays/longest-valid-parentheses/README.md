# 32. Longest Valid Parentheses

**Difficulty:** Hard
**Link:** https://leetcode.com/problems/longest-valid-parentheses/
**Topics:** String, Dynamic Programming, Stack

## Problem

Given a string containing just the characters `'('` and `')'`, return
the length of the longest valid (well-formed) parentheses **substring**
(must be contiguous — not just any subsequence).

### Examples

```
Input: s = "(()"
Output: 2
Explanation: The longest valid parentheses substring is "()".

Input: s = ")()())"
Output: 4
Explanation: The longest valid parentheses substring is "()()".

Input: s = ""
Output: 0
```

### Constraints

- `0 <= s.length <= 3 * 10^4`
- `s[i]` is `'('` or `')'`.

## Approach 1: Brute Force (Check Every Substring)

For every possible `(start, end)` pair, extract the substring and run a
standard balanced-parentheses check on it (a running counter that must
never dip below zero and must land on exactly zero at the end). Keep
the length of the longest one that passes.

- **Time:** `O(n^3)` — `O(n^2)` substrings, `O(n)` to validate each.
- **Space:** `O(n)` for the substring/validation work.

Correct but far too slow for `n` up to `3 * 10^4`.

## Approach 2: Stack of Indices

Push a sentinel `-1` onto the stack first (marking "nothing valid has
matched yet"). Then walk the string:

- `'('` → push its index (a candidate opening bracket).
- `')'` → pop the stack.
  - If the stack becomes **empty**, this `')'` has no match at all —
    push its own index as the new base line for future substrings.
  - Otherwise, the top of the stack now marks the boundary just before
    the current valid run, so the run's length is
    `current_index - stack[-1]`. Update the answer with that.

The sentinel and the "push an unmatched `)`'s index" trick both serve
the same purpose: marking the last position that *can't* be part of a
valid substring, so every subsequent valid run is measured relative to
it.

- **Time:** `O(n)` — each index is pushed and popped at most once.
- **Space:** `O(n)` — worst case (e.g. all `'('`, or all unmatched
  `')'`) the stack holds every index.

## Approach 3: Two-Pass Counters (Optimal — O(1) Space)

Avoid the stack entirely by scanning twice with running counts of
`'('` and `')'`:

**Pass 1 (left → right):** track `open` and `close` counts.
- Whenever `open == close`, we have a balanced run of length
  `2 * close` — update the answer.
- Whenever `close > open`, this position can never be part of a valid
  run starting before it (too many closing brackets) — reset both
  counters to `0`.

This alone under-counts strings where `'('` outnumbers `')'` in a run
(e.g. `"((()"` never triggers a `close > open` reset, so the trailing
valid `"()"` never gets isolated and measured on its own).

**Pass 2 (right → left):** mirror the logic with the roles of `'('`
and `')'` swapped, resetting whenever `open > close`. This catches
exactly the case Pass 1 misses. Together, the two passes cover both
failure modes (excess `')'` and excess `'('`).

- **Time:** `O(n)` — two linear passes over `s`.
- **Space:** `O(1)` — just a few counters.

## Files

- [`solution.py`](./solution.py) — all three approaches
  (`SolutionBruteForce`, `SolutionStack`, and `Solution` for the
  two-pass optimal), plus inline test cases covering the standard
  examples, nested/sequential valid groups, all-unmatched strings, and
  empty input.

## Complexity Summary

| Approach                     | Time   | Space |
|--------------------------------|--------|-------|
| Brute Force (check every substr)| O(n^3) | O(n)  |
| Stack of Indices                | O(n)   | O(n)  |
| Two-Pass Counters (optimal)     | O(n)   | O(1)  |