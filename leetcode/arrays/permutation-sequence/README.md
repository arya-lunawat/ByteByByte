# 46. Permutations

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/permutations/
**Topics:** Array, Backtracking

## Problem

Given an array `nums` of **distinct** integers, return **all possible
permutations**. You can return the answer in any order.

### Examples

```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Input: nums = [0,1]
Output: [[0,1],[1,0]]

Input: nums = [1]
Output: [[1]]
```

### Constraints

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All the integers of `nums` are **unique**.

## Approach 1: Backtracking with a Separate "Used" Array

At each recursive call, try every not-yet-used number as the next
element of the current path: mark it used, append it to the path,
recurse, then undo both (unmark, pop) before trying the next
candidate. When the path reaches length `n`, a full permutation has
been built — copy it into the results.

This is completely standard and correct, but carries a bit of extra
overhead: a separate `used` boolean array (an extra `O(n)` structure
alongside the path itself), and rescanning candidates from the full
`nums` array on every call rather than physically partitioning it into
"already placed" vs. "still available".

- **Time:** `O(n · n!)` — `n!` permutations, `O(n)` to copy each one
  (plus `O(n)` scanning overhead per call for the `used` checks).
- **Space:** `O(n)` for `used`, the recursion stack, and the path —
  plus `O(n · n!)` for the output itself.

## Approach 2: Backtracking via In-Place Swaps (Optimal)

Partition `nums` conceptually into two zones using a single pointer
`start`: indices `[0, start)` hold the permutation prefix chosen so
far, and indices `[start, n)` hold the values still available to
place next. To choose the next element, **swap it into position
`start`** (extending the "chosen" zone by one), recurse on the
remainder, then **swap back** afterward to restore the array for the
next sibling call (undoing the choice).

This eliminates the separate `used` array entirely — "used" is
implicitly encoded by living in the `[0, start)` prefix of the very
array being permuted, and choosing/un-choosing an element is a single
`O(1)` swap rather than a `used[i] = True/False` step layered on top
of a separate path list.

When `start == n`, the array's current arrangement **is** a complete
permutation, so it's copied directly into the results.

- **Time:** `O(n · n!)` — same asymptotic bound as brute force, but
  with a lower constant factor per call: no separate `used` array to
  maintain, no path-list append/pop bookkeeping — just index swaps
  directly on `nums`.
- **Space:** `O(n)` for the recursion stack only — no extra `used`
  array or separate path list needed, since `nums` itself *is* the
  in-progress permutation — plus `O(n · n!)` for the output.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard 3-element example, a 2-element case, a
  single-element case, and a 4-element case checked for the correct
  count (`4! = 24`) and uniqueness of all generated permutations.

## Complexity Summary

| Approach                              | Time       | Space |
|-------------------------------------------|------------|-------|
| Backtracking with `used` array             | O(n · n!)  | O(n)  |
| In-Place Swap Backtracking (optimal)       | O(n · n!)  | O(n)  |

*(Same asymptotic bounds — this is inherently a full-enumeration problem — but the in-place swap version has a lower constant factor per recursive call.)*