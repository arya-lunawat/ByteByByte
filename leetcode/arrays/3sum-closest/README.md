# 16. 3Sum Closest

LeetCode: https://leetcode.com/problems/3sum-closest/
**Difficulty:** Medium

## Problem

Given an integer array `nums` of length `n` and an integer `target`, find
three integers in `nums` whose sum is closest to `target`. Return that
sum. You may assume each input has exactly one solution.

### Examples

| nums | target | Output | Explanation |
|---|---|---|---|
| `[-1,2,1,-4]` | `1` | `2` | `-1+2+1=2` is closest to `1` |
| `[0,0,0]` | `1` | `0` | Only possible sum is `0` |

### Constraints

- `3 <= nums.length <= 500`
- `-1000 <= nums[i] <= 1000`
- `-10^4 <= target <= 10^4`

## Approach

`solution.py` implements two solutions. This problem reuses the same
sort + two-pointer skeleton as **3Sum** (LeetCode 15), just swapping
"find an exact zero-sum triplet" for "track the sum closest to `target`."

### 1. `threeSumClosest` — sort + two pointers (primary)

1. Sort `nums`.
2. Fix one element `nums[i]` at a time as the smallest of the triplet
   (skipping duplicate fixed values, which is just a minor optimization
   here since we're tracking a running best rather than collecting
   distinct triplets).
3. Use two pointers (`left` just after `i`, `right` at the end) to scan
   the rest of the array:
   - Compute the current triplet sum and compare its distance from
     `target` against the best distance seen so far, updating if it's
     closer.
   - If the sum exactly equals `target`, return immediately — no triplet
     can beat a distance of 0.
   - Otherwise move `left` right if the sum is too small, or `right` left
     if it's too large, same as the classic two-pointer sum search.

**Time:** O(n²) — O(n log n) sort + O(n) fixed elements each doing an
O(n) two-pointer sweep.
**Space:** O(1) extra (excluding the sort's own overhead).

### 2. `threeSumClosestBruteForce` — check every triplet (for comparison)

Triple nested loop over all `i < j < k`, tracking the closest sum found.
Correct and simple, but much slower — included to cross-check the
two-pointer result in the test suite.

**Time:** O(n³)
**Space:** O(1)

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (including the problem's own examples, an
all-equal-elements case, a target far outside the array's range, and a
case with several near-tied candidate sums), comparing both solutions
and printing pass/fail for each case.