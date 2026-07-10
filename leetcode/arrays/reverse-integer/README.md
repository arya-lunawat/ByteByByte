# 7. Reverse Integer

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/reverse-integer/

## Problem

Given a signed 32-bit integer `x`, return `x` with its digits reversed. If
reversing `x` causes the value to go outside the signed 32-bit integer
range `[-2^31, 2^31 - 1]`, then return `0`.

Assume the environment does not allow you to store 64-bit integers (signed
or unsigned).

### Example 1
```
Input: x = 123
Output: 321
```

### Example 2
```
Input: x = -123
Output: -321
```

### Example 3
```
Input: x = 120
Output: 21
```

### Constraints
- `-2^31 <= x <= 2^31 - 1`

## Approach: Digit Popping with Overflow Guard

We build the reversed number one digit at a time by repeatedly popping the
last digit off the remaining value and pushing it onto the result:

1. Take the absolute value of `x` and remember its sign separately, so the
   digit-reversal logic doesn't need to special-case negative numbers.
2. While there are digits left:
   - Pop the last digit off (`remaining % 10`), and remove it from
     `remaining` (`remaining //= 10`).
   - **Before** pushing the digit onto `result`, check whether doing so
     would push `result` past `INT_MAX` (`2^31 - 1`). This check must
     happen *before* the multiplication/addition, since the overflowed
     value itself can't safely be computed or compared in a language with
     fixed-width integers.
   - Push the digit onto `result` (`result = result * 10 + digit`).
3. Reapply the original sign to `result`.
4. Do a final range check against `[INT_MIN, INT_MAX]` to safely catch the
   one case where the negative bound (`-2^31`) is one further than the
   positive bound, since Python integers don't naturally overflow like
   fixed-width integers do.
5. Return `0` if the value overflows at any point, otherwise return the
   reversed integer.

### Why check *before* the multiplication?
In languages with fixed-width 32-bit integers, computing
`result * 10 + digit` when it's already too large causes undefined
behavior (overflow) before you'd ever get to check it. The safe pattern is
to algebraically rearrange the overflow condition:

```
result * 10 + digit > INT_MAX
=>  result > (INT_MAX - digit) / 10
```

and check that *before* performing the multiplication. This is the
standard technique for guarding against overflow in integer arithmetic.

## Complexity

| | Complexity |
|---|---|
| Time | `O(log10(x))` — one loop iteration is performed per digit in `x`. |
| Space | `O(1)` — a constant number of variables are used regardless of input size. |

## Alternative Approaches

- **String Reversal** — convert `x` to a string, reverse it, and convert
  back to an integer, handling the sign and overflow separately. Simple to
  write, but relies on string conversion rather than pure arithmetic, and
  many interviewers prefer to see the arithmetic version since it
  generalizes better to environments without built-in big integers.

## Files

- [`solution.py`](./solution.py) — Python solution using digit-by-digit
  reversal with an overflow guard.