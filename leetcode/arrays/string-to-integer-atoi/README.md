# 8. String to Integer (atoi)

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/string-to-integer-atoi/

## Problem

Implement the `myAtoi(string s)` function, which converts a string to a
32-bit signed integer.

The algorithm for `myAtoi(string s)` is as follows:

1. **Whitespace:** Ignore any leading whitespace (`" "`).
2. **Signedness:** Determine the sign by checking if the next character is
   `'-'` or `'+'`, assuming positivity if neither is present.
3. **Conversion:** Read the integer by skipping leading zeros until a
   non-digit character is encountered or the end of the string is reached.
   If no digits were read, then the result is `0`.
4. **Rounding:** If the integer is out of the 32-bit signed integer range
   `[-2^31, 2^31 - 1]`, then round the integer to remain in the range.
   Specifically, integers less than `-2^31` should be rounded to `-2^31`,
   and integers greater than `2^31 - 1` should be rounded to `2^31 - 1`.

Return the integer as the final result.

### Example 1
```
Input: s = "42"
Output: 42
```

### Example 2
```
Input: s = " -042"
Output: -42
```

### Example 3
```
Input: s = "1337c0d3"
Output: 1337
```

### Example 4
```
Input: s = "0-1"
Output: 0
```

### Example 5
```
Input: s = "words and 987"
Output: 0
```

### Constraints
- `0 <= s.length <= 200`
- `s` consists of English letters (lower-case and upper-case), digits
  (0-9), `' '`, `'+'`, `'-'`, and `'.'`.

## Approach: Direct Simulation

This problem is really just about carefully following a state machine /
sequence of rules, one pointer pass through the string:

1. **Skip leading whitespace** — advance a pointer `i` past any leading
   `' '` characters.
2. **Read an optional sign** — if the next character is `'+'` or `'-'`,
   record the sign and advance `i` past it. Only *one* sign character is
   allowed here; anything else (like a second sign, or a space before the
   digits) causes reading to stop at the next step with zero digits found.
3. **Read consecutive digits** — while the current character is a digit,
   build up the result: `result = result * 10 + digit`. Leading zeros are
   naturally absorbed since `0 * 10 + digit` just equals `digit`. Stop as
   soon as a non-digit character is hit or the string ends.
4. **Clamp to the 32-bit range** — check for overflow *before* each
   multiplication (the same technique used in
   [Reverse Integer](../reverse-integer)): if
   `result > (INT_MAX - digit) // 10`, the number is going to overflow, so
   immediately return `INT_MAX` (if positive) or `INT_MIN` (if negative)
   without needing to keep reading further digits.
5. If no digits were ever read, `result` stays `0`, which is returned
   naturally.

### Key Edge Cases Handled
- Empty string or all-whitespace string → `0`.
- No digits after an optional sign (e.g. `"words and 987"`, `"+-12"`) →
  `0`.
- A space *between* the sign and the digits (e.g. `"  +  413"`) is invalid
  per the spec — reading stops immediately since the character right after
  the sign isn't a digit.
- Leading zeros (e.g. `"-042"`) are handled automatically by the
  arithmetic building of `result`.
- Numbers that overflow the 32-bit signed range are clamped rather than
  wrapped or rejected outright.

## Complexity

| | Complexity |
|---|---|
| Time | `O(n)` — the string is scanned once, left to right. |
| Space | `O(1)` — only a few integer/pointer variables are used. |

## Files

- [`solution.py`](./solution.py) — Python solution using direct
  simulation of the atoi algorithm.