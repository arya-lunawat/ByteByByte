# 31. Next Permutation

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/next-permutation/
**Topics:** Array, Two Pointers

## Problem

A permutation of an array of integers is an arrangement of its members
into a sequence or linear order. For example, for `arr = [1,2,3]`, the
permutations in lexicographic order are: `[1,2,3]`, `[1,3,2]`,
`[2,1,3]`, `[2,3,1]`, `[3,1,2]`, `[3,2,1]`.

Given an array of integers `nums`, find **the next permutation** of
`nums` -- i.e. the permutation that comes right after it in
lexicographic order.

If no such arrangement exists (the array is already the *last*
permutation, sorted in fully descending order), rearrange it into the
**lowest** possible order (sorted ascending) instead.

The replacement must be done **in place**, using only **constant extra
memory**.

### Examples

```
Input: nums = [1,2,3]
Output: [1,3,2]

Input: nums = [3,2,1]
Output: [1,2,3]

Input: nums = [1,1,5]
Output: [1,5,1]

Input: nums = [1]
Output: [1]
```

### Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

## Approach 1: Brute Force (Generate All Permutations)

Generate every distinct permutation of `nums`, sort them
lexicographically, locate the current arrangement, and return the one
immediately after it (wrapping around to the first/smallest if the
current one is last).

This directly violates the problem's "constant extra memory"
requirement, but it's a useful correctness baseline.

- **Time:** `O(n! · n log n)` -- `n!` permutations to generate and sort.
- **Space:** `O(n! · n)` -- every permutation has to be stored to sort
  and index into them.

Only practical for tiny arrays; completely infeasible at `n = 100`.

## Approach 2: Pivot, Swap, Reverse (Optimal, In-Place)

Think of `nums` as digits of a number. To get the *next* larger
arrangement with the *smallest possible increase*, we want to change
digits as far to the right (least significant) as possible.

1. **Find the pivot.** Scan from the right for the first index `i`
   where `nums[i] < nums[i + 1]`. Everything to the right of `i` is
   currently non-increasing -- i.e. already the largest arrangement
   possible for that suffix -- so no improvement is possible there
   without touching `nums[i]`.
2. **No pivot found?** The whole array is non-increasing, meaning it's
   already the last permutation. Reverse the entire array to wrap
   around to the smallest (fully ascending) permutation, and stop.
3. **Find the swap partner.** Scan from the right again for the
   smallest value in the suffix that's still greater than `nums[i]`.
   Since the suffix is non-increasing, this is just the *rightmost*
   value greater than `nums[i]` -- picking the rightmost (not the
   first found) is what correctly handles duplicate values. Swap it
   with `nums[i]`.
4. **Reverse the suffix.** After the swap, the suffix (everything after
   index `i`) is still non-increasing; reversing it makes it ascending
   -- the smallest possible arrangement for those values -- which
   guarantees the overall increase from the original array is as small
   as possible.

- **Time:** `O(n)` -- at most three linear passes over `nums`.
- **Space:** `O(1)` -- everything is done in place with index swaps.

## Files

- [`solution.py`](./solution.py) -- both approaches (`SolutionBruteForce`
  and `Solution`), plus inline test cases covering the standard
  examples, duplicate values, mid-sequence permutations, and the
  descending-array wraparound case.

## Complexity Summary

| Approach                        | Time            | Space   |
|-----------------------------------|-----------------|---------|
| Brute Force (generate all perms)  | O(n! · n log n) | O(n! · n) |
| Pivot, Swap, Reverse               | O(n)            | O(1)    |