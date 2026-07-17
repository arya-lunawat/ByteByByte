# 35. Search Insert Position

**Difficulty:** Easy
**Link:** https://leetcode.com/problems/search-insert-position/
**Topics:** Array, Binary Search

## Problem

Given a sorted array of **distinct** integers `nums` and a `target`
value, return the index if `target` is found. If not, return the
index where it would be if it were inserted in order to keep `nums`
sorted.

You must write an algorithm with **`O(log n)`** runtime complexity.

### Examples

```
Input: nums = [1,3,5,6], target = 5
Output: 2

Input: nums = [1,3,5,6], target = 2
Output: 1

Input: nums = [1,3,5,6], target = 7
Output: 4
```

### Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` contains **distinct** values sorted in **ascending** order.
- `-10^4 <= target <= 10^4`

## Approach 1: Brute Force (Linear Scan)

Walk the array left to right and return the first index whose value is
`>= target` — that's exactly where `target` belongs, whether or not
it's already present. If no such index exists, `target` is larger than
every element, so it belongs at the very end (`len(nums)`).

- **Time:** `O(n)`
- **Space:** `O(1)`

Correct, but doesn't meet the required `O(log n)` runtime — included
as a baseline.

## Approach 2: Binary Search for the Leftmost Insertion Point (Optimal)

This is standard binary search with a different stopping question:
instead of "does `nums[mid]` equal `target`?", we ask "could a valid
insertion point still be at or before `mid`, or must it be strictly
after?"

- If `nums[mid] < target`, the insertion point has to be somewhere
  after `mid` → `low = mid + 1`.
- Otherwise (`nums[mid] >= target`), `mid` is a valid candidate (either
  the exact match or a value `target` should be inserted before) → keep
  narrowing left with `high = mid - 1` to see if an even earlier valid
  spot exists.

When `low` and `high` cross and the loop ends, `low` has converged
exactly to the correct insertion index — landing on the match itself
if `target` is present (values are distinct), or on the correct gap if
it isn't.

- **Time:** `O(log n)`
- **Space:** `O(1)`

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering an exact match, insertion in the middle, insertion at the
  very start, insertion at the very end, and a single-element array.

## Complexity Summary

| Approach                        | Time     | Space |
|------------------------------------|----------|-------|
| Brute Force (linear scan)          | O(n)     | O(1)  |
| Binary Search (leftmost insertion) | O(log n) | O(1)  |