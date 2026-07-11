# 9. Palindrome Number

LeetCode: https://leetcode.com/problems/palindrome-number/description/
**Difficulty:** Easy

## Problem

Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.

A number is a palindrome when it reads the same forward and backward.

### Examples

| Input | Output | Explanation |
|---|---|---|
| `x = 121` | `true` | Reads the same both ways |
| `x = -121` | `false` | Reversed it's `121-`, which isn't valid |
| `x = 10` | `false` | Reversed it's `01`, which isn't equal to `10` |

### Constraints

- `-2^31 <= x <= 2^31 - 1`

**Follow-up:** Could you solve it without converting the integer to a string?

## Approach

`solution.py` implements two versions:

### 1. `isPalindrome` — reverse half the number (no string conversion)

- Negative numbers are immediately `false` (the `-` sign can never mirror).
- Numbers ending in `0` are `false`, unless the number itself is `0`, since a
  palindrome can't have a leading zero.
- We build up `reverted_half` by repeatedly peeling off the last digit of `x`
  and appending it, while shrinking `x`, until `x <= reverted_half`. At that
  point we've reversed the second half of the digits.
- If the digit count is even, `x == reverted_half`.
  If it's odd, the middle digit sits in `reverted_half`'s last position, so we
  drop it with `reverted_half // 10` before comparing.

**Time:** O(log₁₀ x) — proportional to the number of digits
**Space:** O(1)

### 2. `isPalindromeString` — simple string reversal (for comparison)

Converts `x` to a string and checks it against its reverse (`s == s[::-1]`).
Simple and readable, but uses O(n) extra space and doesn't satisfy the
follow-up constraint.

**Time:** O(n) where n is the number of digits
**Space:** O(n)

## Running

```bash
python3 solution.py
```

This runs a small built-in test suite (including edge cases like `0`,
single-digit numbers, negative numbers, numbers ending in `0`, and
`2^31 - 1`) and prints pass/fail status for each case.