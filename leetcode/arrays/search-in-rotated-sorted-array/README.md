# 33. Search in Rotated Sorted Array

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/search-in-rotated-sorted-array/
**Topics:** Array, Binary Search

## Problem

There is an integer array `nums` sorted in **ascending order** (with
**distinct** values).

Prior to being passed to your function, `nums` is possibly **rotated**
at an unknown pivot index `k` such that the resulting array is
`[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`
(0-indexed). For example, `[0,1,2,4,5,6,7]` might be rotated at pivot
index `3` to become `[4,5,6,7,0,1,2]`.

Given `nums` after the possible rotation and an integer `target`,
return the index of `target` if it is in `nums`, or `-1` if it is not.

You must write an algorithm with **`O(log n)`** runtime complexity.

### Examples

```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Input: nums = [1], target = 0
Output: -1
```

### Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are **unique**.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

## Approach 1: Brute Force (Linear Scan)

Just walk the array and compare each element to `target`. Completely
ignores the sorted/rotated structure, and doesn't satisfy the problem's
required `O(log n)` runtime — included only as a correctness baseline.

- **Time:** `O(n)`
- **Space:** `O(1)`

## Approach 2: Modified Binary Search (Optimal)

A rotated sorted array is really just two sorted halves glued together
at the rotation point. The key insight: at any search window
`[low, high]`, splitting it at `mid` guarantees **at least one of the
two halves is fully sorted** — so on every iteration we can:

1. Check if `nums[mid] == target` — done if so.
2. Figure out which half is sorted:
   - If `nums[low] <= nums[mid]`, the **left** half `[low, mid]` is
     sorted.
     - If `target` falls inside `[nums[low], nums[mid])`, search left.
     - Otherwise, it must be in the right half — search right.
   - Otherwise, the **right** half `[mid, high]` is sorted.
     - If `target` falls inside `(nums[mid], nums[high]]`, search
       right.
     - Otherwise, search left.

Each iteration discards roughly half the search space — same as
classic binary search — just with one extra check up front to decide
which half's ordering we can actually trust.

- **Time:** `O(log n)`
- **Space:** `O(1)`

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard examples, a single-element array, small
  2-3 element rotations, an unrotated array, and searching for values
  at both ends of the rotation.

## Complexity Summary

| Approach                  | Time     | Space |
|-----------------------------|----------|-------|
| Brute Force (linear scan)   | O(n)     | O(1)  |
| Modified Binary Search       | O(log n) | O(1)  |