# 29. Divide Two Integers

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/divide-two-integers/
**Topics:** Math, Bit Manipulation

## Problem

Given two integers `dividend` and `divisor`, divide them **without using
multiplication, division, or the mod operator**.

The division should **truncate toward zero** (e.g. `8.345 -> 8`, `-2.7335 -> -2`).

Return the quotient after dividing `dividend` by `divisor`.

> **Note:** Assume the environment can only store 32-bit signed integers:
> `[-2^31, 2^31 - 1]`. If the quotient is strictly greater than `2^31 - 1`,
> return `2^31 - 1`. If it's strictly less than `-2^31`, return `-2^31`.

### Examples

```
Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10 / 3 = 3.33333.. which is truncated to 3.

Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7 / -3 = -2.33333.. which is truncated to -2.
```

### Constraints

- `-2^31 <= dividend, divisor <= 2^31 - 1`
- `divisor != 0`

## Approach 1: Brute Force (Repeated Subtraction)

Strip the signs, then repeatedly subtract `|divisor|` from `|dividend|`,
counting how many subtractions happen. Reapply the sign at the end and
clamp to the 32-bit range.

- **Time:** `O(dividend / divisor)` — degenerates badly when the divisor
  is small relative to the dividend (e.g. dividing by 1), so this
  **can TLE** on large inputs.
- **Space:** `O(1)`

## Approach 2: Bit-Shift Doubling (Optimal)

Instead of peeling off one `divisor` at a time, peel off the **largest
power-of-two multiple** of the divisor that still fits, using left shifts
(`temp + temp`) to double it. Subtract that chunk, add the matching power
of two to the quotient, and repeat on what's left — this is essentially
binary long division.

Handle the one true overflow case up front: `INT_MIN / -1` would be
`2^31`, which doesn't fit in a signed 32-bit int, so it's clamped to
`INT_MAX` immediately.

- **Time:** `O(log^2(dividend))` — outer loop runs `O(log n)` times,
  inner doubling loop also `O(log n)` times.
- **Space:** `O(1)`

## Files

- [`solution.py`](./solution.py) — both approaches (`SolutionBruteForce`
  and `Solution`), plus inline test cases covering the standard examples
  and edge cases (zero, sign combinations, overflow clamp).

## Complexity Summary

| Approach              | Time            | Space |
|------------------------|-----------------|-------|
| Brute Force (subtract)  | O(dividend/divisor) | O(1) |
| Bit-Shift Doubling      | O(log^2 n)      | O(1)  |