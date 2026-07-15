# 28. Find the Index of the First Occurrence in a String

LeetCode: https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
**Difficulty:** Easy

## Problem

Given two strings `needle` and `haystack`, return the index of the first
occurrence of `needle` in `haystack`, or `-1` if `needle` isn't a
substring of `haystack`. (This is the classic `strStr()` problem.)

### Examples

| haystack | needle | Output | Explanation |
|---|---|---|---|
| `"sadbutsad"` | `"sad"` | `0` | First match starts at index 0 |
| `"leetcode"` | `"leeto"` | `-1` | No match anywhere |

### Constraints

- `1 <= haystack.length, needle.length <= 10^4`
- Both strings consist only of lowercase English letters

## Approach

`solution.py` implements two solutions.

### 1. `strStr` — KMP (Knuth-Morris-Pratt) (primary)

The naive approach can waste work: when a mismatch occurs partway
through a candidate match, it re-scans haystack characters that were
already known to match the needle's prefix. KMP avoids this by
precomputing an **LPS table** ("longest proper prefix that's also a
suffix") for `needle` itself.

- `lps[i]` = the length of the longest proper prefix of `needle[0:i+1]`
  that's also a suffix of that same substring.
- While scanning `haystack` with pointer `i` and matching against
  `needle` with pointer `j`: on a mismatch (with `j > 0`), instead of
  resetting `j` to `0` and re-checking characters we already know match,
  jump `j` directly to `lps[j-1]` — the longest prefix of `needle` that
  could still align with what's already matched, so no haystack
  character ever needs to be re-examined.
- On a full match (`j` reaches `len(needle)`), the match started at
  `i - j`.

This guarantees the haystack pointer `i` never moves backward, which is
what gives KMP its linear time bound.

**Time:** O(n + m) where `n = len(haystack)`, `m = len(needle)` — O(m) to
build the LPS table, O(n) to scan haystack.
**Space:** O(m) for the LPS table.

### 2. `strStrNaive` — brute-force substring check (for comparison)

Tries every starting position in `haystack` and directly compares the
substring there against `needle`. Simple and, given this problem's small
constraints (`10^4`), often fast enough in practice — but its worst case
is much worse than KMP's, e.g. `haystack = "aaaa...a"`,
`needle = "aaa...b"` triggers a near-full re-comparison at almost every
position.

**Time:** O(n × m) worst case.
**Space:** O(1) extra (aside from the string slices Python creates for
comparison).

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (covering the problem's own examples, a
single-character exact match, a match at the very end of the string, no
match at all, and a case specifically designed to exercise KMP's
fallback jump — `"aabaaabaaac"` / `"aabaaac"`, where a naive scan would
backtrack but KMP does not), comparing both solutions and printing
pass/fail for each case.