# 43. Multiply Strings

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/multiply-strings/
**Topics:** Math, String, Simulation

## Problem

Given two non-negative integers `num1` and `num2` represented as
strings, return the product of `num1` and `num2`, also represented as
a string.

> **Note:** You must not use any built-in BigInteger library or
> convert the inputs to integers directly.

### Examples

```
Input: num1 = "2", num2 = "3"
Output: "6"

Input: num1 = "123", num2 = "456"
Output: "56088"
```

### Constraints

- `1 <= num1.length, num2.length <= 200`
- `num1` and `num2` consist of digits only.
- Both `num1` and `num2` do not contain any leading zero, except the
  number `0` itself.

## Approach 1: Convert to Native Ints (Baseline Only — Violates the Rules)

`int(num1) * int(num2)`, converted back to a string. This is exactly
what the problem explicitly forbids — it hands the actual
multiplication off to Python's built-in arbitrary-precision integers
instead of implementing it by hand. Included purely as a correctness
sanity check to validate the real solution against, not as a
legitimate submission.

- **Time:** Depends entirely on Python's internal big-int
  multiplication algorithm — not a meaningful measurement of the
  intended technique.
- **Space:** `O(len(num1) + len(num2))` for the string conversions.

## Approach 2: Grade-School Digit-by-Digit Multiplication (Optimal)

Mirrors how you'd multiply two numbers by hand on paper, using only an
array of partial results — no built-in big-integer arithmetic.

For numbers of length `m` and `n`, the product has **at most `m + n`
digits**. Allocate a result array `product` of that size, all zeros.

For every pair of digits `num1[i]` and `num2[j]` (indexed from the
left in the string), their product contributes to two **adjacent**
positions in the result array: the low digit lands at `i + j + 1`, and
any carry-out bumps into `i + j`. We **add** each partial product into
`product[i + j + 1]` (rather than assign), since multiple digit pairs
can land on the same result position — exactly like how, in long
multiplication by hand, several columns get summed together before you
carry.

After every digit pair has been processed, some slots in `product` may
still hold values greater than 9 (unresolved carries from the addition
step above). Since digit pairs are processed in decreasing significance
order and carries are folded into `total // 10` immediately at each
step, no separate carry-propagation pass is needed — the accumulation
itself handles it.

Finally, convert the digit array to a string, skipping leading zeros
(but keeping at least one digit so `"0" * "anything"` still returns
`"0"`), with a quick early return if either input is literally `"0"`.

- **Time:** `O(m · n)` — every pair of digits (one from each number)
  is visited exactly once to compute and accumulate its contribution.
- **Space:** `O(m + n)` — the result digit array.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering single-digit products, multi-digit products, zero inputs,
  and a large 9-digit × 9-digit multiplication to stress-test carry
  handling.

## Complexity Summary

| Approach                                  | Time     | Space |
|-----------------------------------------------|----------|-------|
| Native int conversion (baseline, not allowed)   | Implementation-defined | O(m + n) |
| Grade-School Digit-by-Digit (optimal)           | O(m · n) | O(m + n) |