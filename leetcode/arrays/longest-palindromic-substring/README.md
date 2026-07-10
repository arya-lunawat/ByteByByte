# 5. Longest Palindromic Substring

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/longest-palindromic-substring/

## Problem

Given a string `s`, return the longest palindromic substring in `s`.

### Example 1
```
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.
```

### Example 2
```
Input: s = "cbbd"
Output: "bb"
```

### Constraints
- `1 <= s.length <= 1000`
- `s` consist of only digits and English letters.

## Approach: Expand Around Center

A palindrome mirrors around its center, so instead of checking every
substring (which is `O(n^3)` naively), we can check every possible **center**
and expand outward while the characters on each side match.

There are `2n - 1` possible centers for a string of length `n`:
- `n` centers where the palindrome has odd length (a single character center,
  e.g. `"aba"` centers on `"b"`).
- `n - 1` centers where the palindrome has even length (a center between two
  characters, e.g. `"abba"` centers between the two `"b"`s).

For each index `i`, we expand around both:
1. `(i, i)` — odd-length case
2. `(i, i + 1)` — even-length case

and keep track of the longest palindrome found so far.

### Steps
1. Iterate over each index `i` in the string.
2. Expand around center `(i, i)` to find the longest odd-length palindrome
   centered at `i`.
3. Expand around center `(i, i + 1)` to find the longest even-length
   palindrome centered between `i` and `i + 1`.
4. If either expansion produces a palindrome longer than the best one found
   so far, update the recorded start and end indices.
5. Return the substring defined by the best start/end indices.

## Complexity

| | Complexity |
|---|---|
| Time | `O(n^2)` — there are `O(n)` centers, and each expansion can take up to `O(n)` steps. |
| Space | `O(1)` — only a few pointers/indices are used besides the returned substring. |

## Alternative Approaches

- **Brute Force** — check every substring for being a palindrome:
  `O(n^3)` time, `O(1)` space.
- **Dynamic Programming** — `dp[i][j]` = whether `s[i..j]` is a palindrome,
  built from smaller substrings outward: `O(n^2)` time, `O(n^2)` space.
- **Manacher's Algorithm** — computes the answer in `O(n)` time using a
  clever transformation of the string, at the cost of higher implementation
  complexity.

## Files

- [`solution.py`](./solution.py) — Python solution using the Expand Around
  Center approach.