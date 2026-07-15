# 26. Remove Duplicates from Sorted Array

LeetCode: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
**Difficulty:** Easy

## Problem

Given an integer array `nums` sorted in non-decreasing order, remove
duplicates **in-place** so each unique element appears only once,
preserving relative order. Return `k`, the number of unique elements;
the first `k` slots of `nums` must hold those unique values in their
original order (the rest of the array doesn't matter).

### Examples

| nums | Output | nums after |
|---|---|---|
| `[1,1,2]` | `2` | `[1,2,_]` |
| `[0,0,1,1,1,2,2,3,3,4]` | `5` | `[0,1,2,3,4,_,_,_,_,_]` |

### Constraints

- `1 <= nums.length <= 3 * 10^4`
- `-100 <= nums[i] <= 100`
- `nums` is sorted in non-decreasing order

## Approach

`solution.py` implements two solutions.

### 1. `removeDuplicates` — two pointers, in-place (primary)

Because the array is **sorted**, every duplicate of a value sits right
next to its other copies — no need for a hash set or any lookup
structure to detect duplicates.

- `write` tracks the boundary of the unique-elements-so-far region
  (everything before it is finalized and unique). It starts at `1`,
  since `nums[0]` is trivially unique (nothing comes before it).
- `read` scans forward from index `1`. Whenever `nums[read]` differs from
  the last *written* unique value (`nums[write - 1]`), it's a new unique
  value — copy it to `nums[write]` and advance `write`.
- Values equal to the last written one are duplicates and are simply
  skipped by `read` continuing to advance without touching `write`.

By the end, `nums[0:write]` holds exactly the unique values in original
order, and `write` is the answer `k`.

**Time:** O(n) — single pass with two pointers.
**Space:** O(1) — modifies `nums` in place, no auxiliary structures.

### 2. `removeDuplicatesSet` — build a unique list, then copy back (for comparison)

Scans through `nums` once, appending a value to an `unique` list only
when it differs from the last appended value (this still relies on
sortedness to keep duplicates adjacent — a true hash-set approach would
be unnecessary here). Then copies `unique` back into the front of
`nums`. Functionally equivalent, but uses O(n) extra space for the
intermediate list rather than working purely in-place.

**Time:** O(n)
**Space:** O(n) for the intermediate `unique` list.

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (covering the problem's own examples, a
single-element array, an array that's entirely one repeated value, an
array with no duplicates at all, and negative values), checking both the
returned `k` and the resulting prefix `nums[:k]` against expected values
for both solutions, printing pass/fail for each case.