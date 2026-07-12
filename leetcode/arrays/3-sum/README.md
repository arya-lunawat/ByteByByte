# 15. 3Sum

LeetCode: https://leetcode.com/problems/3sum/
**Difficulty:** Medium

## Problem

Given an integer array `nums`, return all the triplets
`[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, `j != k`, and
`nums[i] + nums[j] + nums[k] == 0`.

The solution set must not contain duplicate triplets.

### Examples

| nums | Output | Explanation |
|---|---|---|
| `[-1,0,1,2,-1,-4]` | `[[-1,-1,2],[-1,0,1]]` | Two distinct zero-sum triplets exist |
| `[0,1,1]` | `[]` | No triplet sums to 0 |
| `[0,0,0]` | `[[0,0,0]]` | The only triplet, and it works |

### Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Approach

`solution.py` implements two solutions. Both sort the array up front,
which turns "find all zero-sum triplets" into a variant of the classic
sorted-array two-pointer Two Sum problem, repeated once per fixed element.

### 1. `threeSum` — sort + two pointers (primary)

1. Sort `nums`.
2. Fix one element `nums[i]` at a time as the smallest of the triplet.
   - If `nums[i] > 0`, no triplet from here on can sum to zero (everything
     after it is `>= nums[i] > 0`), so we can stop entirely.
   - Skip over duplicate values of `nums[i]` so the same fixed value isn't
     processed twice.
3. For the remainder of the array (`i+1` to end), use two pointers —
   `left` just after `i`, `right` at the end — to find pairs summing to
   `-nums[i]`, moving inward based on whether the current pair sum is too
   small or too large. When a match is found, skip past any duplicate
   values at both pointers before continuing, so no duplicate triplet is
   ever added.

**Time:** O(n²) — O(n log n) for the sort, then O(n) fixed elements each
doing an O(n) two-pointer sweep.
**Space:** O(1) extra (not counting the output and the sort's own
overhead).

### 2. `threeSumHashSet` — sort + hash set (for comparison)

Same outer loop over the fixed element `nums[i]`, but instead of two
pointers, scans forward once using a hash set to check whether the
complement needed to reach zero has already been seen. Duplicate triplets
are avoided by skipping repeated values of the fixed element and of the
inner scan variable.

**Time:** O(n²) — O(n) fixed elements each doing an O(n) hash-set scan.
**Space:** O(n) for the hash set, reset for each fixed element.

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (including the classic example, all-zero
arrays, arrays with heavy duplication, and a no-solution case). Since
triplet order and result order aren't required to match LeetCode's
example output exactly, the test harness normalizes both the expected
and actual results (sorting each triplet's elements and sorting the list
of triplets) before comparing, and prints pass/fail for each case.