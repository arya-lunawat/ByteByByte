# 41. First Missing Positive

**Difficulty:** Hard
**Link:** https://leetcode.com/problems/first-missing-positive/
**Topics:** Array, Hash Table

## Problem

Given an unsorted integer array `nums`, return the **smallest missing
positive integer**.

You must implement an algorithm that runs in **`O(n)` time** and uses
**`O(1)` auxiliary space**.

### Examples

```
Input: nums = [1,2,0]
Output: 3
Explanation: The numbers in the range [1,2] are all in the array.

Input: nums = [3,4,-1,1]
Output: 2
Explanation: 1 is in the array but 2 is missing.

Input: nums = [7,8,9,11,12]
Output: 1
Explanation: The smallest positive integer 1 is missing.
```

### Constraints

- `1 <= nums.length <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`

## Approach 1: Hash Set + Linear Probe

Dump every number into a set for `O(1)` membership checks. Then,
starting from `1`, keep asking "is `k` in the set?" and incrementing
`k` until one isn't found. Since an array of `n` numbers can "block" at
most the values `1` through `n`, the answer is guaranteed to be
somewhere in `[1, n + 1]` — so this probe loop runs at most `n + 1`
times.

This satisfies the `O(n)` **time** requirement but uses `O(n)`
auxiliary space for the set, violating the problem's `O(1)` space
constraint. Included as a simpler correctness baseline.

- **Time:** `O(n)` — one pass to build the set, up to `n + 1` probes.
- **Space:** `O(n)` — the hash set.

## Approach 2: In-Place Cyclic Placement (Optimal)

The insight that unlocks `O(1)` space: the answer must lie in
`[1, n + 1]` where `n = len(nums)`. So any value outside `[1, n]` is
irrelevant to the final answer, and any value `v` inside `[1, n]`
"belongs" at index `v - 1` in a fully sorted, gap-free arrangement
(`nums[0]` should hold `1`, `nums[1]` should hold `2`, and so on).

**Pass 1 — place values where they belong.** For each index `i`, if
`nums[i]` is in range (`1 <= nums[i] <= n`) and it isn't already
sitting in its correct home slot, swap it there. Keep checking the
*same* index after each swap (a `while`, not an `if`) since the
newly-swapped-in value might also need to move on. Values that are
`<= 0`, `> n`, or duplicates of what's already correctly placed at
their target slot are simply left alone — they can never be the
answer.

**Pass 2 — find the first mismatch.** Scan left to right; the first
index `i` where `nums[i] != i + 1` means `i + 1` is the smallest
missing positive. If every slot matches (the array ends up exactly
`[1, 2, ..., n]`), the answer is `n + 1`.

Every value is swapped into its final resting place **at most once**
across the whole process — once correctly placed, a value is never
touched again — so despite the nested-looking `while` loop, total work
across both passes stays linear.

- **Time:** `O(n)` — each index triggers at most one chain of swaps,
  and every value moves into place at most once overall.
- **Space:** `O(1)` — rearranges `nums` in place, no extra data
  structures.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard examples, an empty array, an already-complete
  `[1..n]` array, duplicate values, and all-non-positive input.

## Complexity Summary

| Approach                              | Time | Space |
|------------------------------------------|------|-------|
| Hash Set + Linear Probe                    | O(n) | O(n)  |
| In-Place Cyclic Placement (optimal)        | O(n) | O(1)  |