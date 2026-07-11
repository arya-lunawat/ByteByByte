# 11. Container With Most Water

LeetCode: https://leetcode.com/problems/container-with-most-water/
**Difficulty:** Medium

## Problem

You are given an integer array `height` of length `n`. There are `n`
vertical lines drawn such that the two endpoints of the `i`-th line are
`(i, 0)` and `(i, height[i])`.

Find two lines that, together with the x-axis, form a container that holds
the most water. Return the maximum amount of water a container can store.
The container cannot be slanted.

### Examples

| height | Output | Explanation |
|---|---|---|
| `[1,8,6,2,5,4,8,3,7]` | `49` | Lines at index 1 (height 8) and index 8 (height 7): `min(8,7) * (8-1) = 49` |
| `[1,1]` | `1` | Only one possible container: `min(1,1) * 1 = 1` |

### Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Approach

`solution.py` implements two solutions.

### 1. `maxArea` — two pointers (optimal)

Start with pointers at the two ends of the array — the widest possible
container. The area of any container is `min(height[left], height[right]) *
(right - left)`, so it's always capped by the **shorter** line.

- If we move the pointer at the **taller** line inward, the width shrinks
  and the limiting height can only stay the same or get smaller (since it
  was already set by the shorter side) — this can never improve the area.
- If we move the pointer at the **shorter** line inward, the width still
  shrinks, but we might find a taller line, which *could* increase the
  limiting height enough to beat the previous area.

So the greedy rule is: **always move the pointer at the shorter line
inward**, recording the best area seen at each step. Since each step
moves one pointer and we stop when they meet, we cover the whole array in
one linear pass without missing the optimal pair.

**Time:** O(n) — single pass
**Space:** O(1)

### 2. `maxAreaBruteForce` — check every pair (for comparison)

Tries every pair `(i, j)` and takes the best area. Correct but slow —
included mainly to sanity-check the two-pointer result in the test suite.

**Time:** O(n²)
**Space:** O(1)

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (including the classic examples, all-equal
heights, ascending heights, and a zero-height edge case), comparing the
two-pointer and brute-force results and printing pass/fail for each case.