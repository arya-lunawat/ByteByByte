# 38. Count and Say

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/count-and-say/
**Topics:** String

## Problem

The count-and-say sequence is a sequence of digit strings defined by
the recursive formula:

- `countAndSay(1) = "1"`
- `countAndSay(n)` is the **run-length encoding** of `countAndSay(n - 1)`.

Run-length encoding (RLE) replaces consecutive identical characters
(each run of 2 or more) with the run's count followed by the
character. For example, `"3322251"` becomes `"23321511"`:
`"33"` → `"23"`, `"222"` → `"32"`, `"5"` → `"15"`, `"1"` → `"11"`.

Given a positive integer `n`, return the `n`th term of the
count-and-say sequence.

### Examples

```
Input: n = 1
Output: "1"
Explanation: This is the base case.

Input: n = 4
Output: "1211"
Explanation:
  countAndSay(1) = "1"
  countAndSay(2) = RLE of "1" = "11"
  countAndSay(3) = RLE of "11" = "21"
  countAndSay(4) = RLE of "21" = "1211"
```

### Constraints

- `1 <= n <= 30`

## Approach 1: Brute Force (Naive String Concatenation)

Start from `"1"` and, for `n - 1` iterations, scan the current term
character by character. Whenever a run of identical characters ends,
append its count and character onto the result using `result += ...`.

Python strings are immutable, so every `+=` creates a **brand-new
string** and copies the old contents into it. Doing this repeatedly
while building each term means the string-building itself degrades to
`O(L^2)` for a term of length `L`, on top of the `O(L)` scan of the
previous term — an anti-pattern compared to deferring all the pieces
into one join at the end.

- **Time:** Still fast in practice here since `n <= 30` keeps term
  lengths small, but the repeated `+=` concatenation is `O(L^2)` per
  term rather than `O(L)`.
- **Space:** `O(L)` for the current/next strings, `L` = length of the
  longest term generated.

## Approach 2: Two-Pointer RLE with List-Based Building (Optimal)

Same core recurrence, but avoids the concatenation pitfall: instead of
growing a string with repeated `+=`, collect each run's `count` and
`char` into a list, then build the term with a **single**
`''.join(...)` call. List appends are amortized `O(1)`, and the final
join is `O(L)` for a term of length `L` — no repeated copying.

The scan itself uses two pointers (`i` marking the start of a run, `j`
advancing while characters match) to find run boundaries in one linear
pass per term.

- **Time:** `O(sum of term lengths)` across all `n` terms — each term
  is built in `O(L)` rather than `O(L^2)`.
- **Space:** `O(L)` for the current term and the list building the
  next one, `L` = length of the longest term generated.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the first 8 terms of the sequence (`n = 1` through `n = 8`),
  verified against the well-known values.

## Complexity Summary

| Approach                              | Time (per term of length L) | Space |
|------------------------------------------|------------------------------|-------|
| Brute Force (string `+=` concatenation)   | O(L^2)                       | O(L)  |
| Two-Pointer RLE + list `join` (optimal)   | O(L)                          | O(L)  |