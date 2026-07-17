# 34. Find First and Last Position of Element in Sorted Array

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
**Topics:** Array, Binary Search

## Problem

Given an array of integers `nums` sorted in **non-decreasing** order,
find the starting and ending position of a given `target` value.

If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with **`O(log n)`** runtime complexity.

### Examples

```
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Input: nums = [], target = 0
Output: [-1,-1]
```

### Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums` is a non-decreasing array.
- `-10^9 <= target <= 10^9`

## Approach 1: Brute Force (Linear Scan)

Walk the array once, remembering the first index where `nums[i] ==
target` and continuously updating the last index where that's true.
Correct, but doesn't meet the required `O(log n)` runtime — included
as a correctness baseline.

- **Time:** `O(n)`
- **Space:** `O(1)`

## Approach 2: Two Binary Searches — Leftmost & Rightmost Bound (Optimal)

A plain binary search stops as soon as it hits any occurrence of
`target`, which tells you nothing about where the run of duplicates
starts or ends. The fix is to bias the search in a chosen direction
*even after finding a match*, run twice:

- **Find the first occurrence:** whenever `nums[mid] == target`,
  record `mid` as a candidate but keep searching the **left** half
  (`high = mid - 1`) in case an earlier occurrence exists.
- **Find the last occurrence:** symmetric — record `mid`, but keep
  searching the **right** half (`low = mid + 1`) to push the candidate
  as late as possible.

In both searches, the "not found yet" comparisons behave exactly like
standard binary search (`nums[mid] < target` → `low = mid + 1`,
`nums[mid] > target` → `high = mid - 1`); only what happens on a match
differs between the two passes.

If the first search comes back `-1`, the target isn't present at all,
so we can skip the second search and return `[-1, -1]` immediately.

- **Time:** `O(log n)` — two independent binary searches.
- **Space:** `O(1)`

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard examples, an empty array, a single-element
  array, an all-duplicates array, and target values at the very start
  or end of the array.

## Complexity Summary

| Approach                          | Time     | Space |
|-------------------------------------|----------|-------|
| Brute Force (linear scan)           | O(n)     | O(1)  |
| Two Binary Searches (leftmost/rightmost) | O(log n) | O(1)  |