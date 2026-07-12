# 14. Longest Common Prefix

LeetCode: https://leetcode.com/problems/longest-common-prefix/
**Difficulty:** Easy

## Problem

Write a function to find the longest common prefix string amongst an
array of strings. If there is no common prefix, return an empty string
`""`.

### Examples

| strs | Output | Explanation |
|---|---|---|
| `["flower","flow","flight"]` | `"fl"` | All three start with `"fl"` |
| `["dog","racecar","car"]` | `""` | No shared starting characters |

### Constraints

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` consists of only lowercase English letters.

## Approach

`solution.py` implements two solutions.

### 1. `longestCommonPrefix` — vertical scanning (primary)

Any common prefix can be no longer than the shortest string in the array,
so that string is a natural upper bound. Walk through its characters one
position at a time (a "column"), and at each position check whether every
other string has the same character there. The moment a mismatch is
found, the prefix ends right there — return everything scanned so far.
If we make it through the whole shortest string without a mismatch, the
entire shortest string is the answer.

**Time:** O(S) where S is the total number of characters across all
strings — worst case scans every character of the shortest string against
every other string.
**Space:** O(1) extra, aside from the returned string.

### 2. `longestCommonPrefixSort` — sort first (for comparison)

Sort the array lexicographically. Once sorted, the common prefix of the
*whole array* is guaranteed to equal the common prefix of just the
**first and last** strings — any string in between is lexicographically
"between" them, so it can't diverge from the shared prefix any earlier
than they do. This reduces the problem to comparing just two strings
after sorting.

**Time:** O(S log n) — dominated by the sort (each comparison can take up
to O(S/n) characters), plus a final O(m) prefix scan.
**Space:** O(n) auxiliary space for the sort (Python's Timsort).

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (including the classic examples, a
single-element array, an empty-string edge case, no-common-prefix cases,
and a case where a shorter string is itself a prefix of a longer one),
comparing both solutions and printing pass/fail for each case.