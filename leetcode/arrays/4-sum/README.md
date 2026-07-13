# 18. 4Sum

LeetCode: https://leetcode.com/problems/4sum/
**Difficulty:** Medium

## Problem

Given an array `nums` of `n` integers and an integer `target`, return all
unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that
`a, b, c, d` are distinct indices and
`nums[a] + nums[b] + nums[c] + nums[d] == target`.

### Examples

| nums | target | Output |
|---|---|---|
| `[1,0,-1,0,-2,2]` | `0` | `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]` |
| `[2,2,2,2,2]` | `8` | `[[2,2,2,2]]` |

### Constraints

- `1 <= nums.length <= 200`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`

## Approach

`solution.py` implements two solutions. This problem is a direct
generalization of **3Sum** (LeetCode 15) with one extra fixed element.

### 1. `fourSum` — sort + two nested fixed elements + two pointers (primary)

1. Sort `nums`.
2. Fix the first element `nums[i]` with an outer loop, skipping duplicate
   values.
3. Fix the second element `nums[j]` with an inner loop (starting after
   `i`), also skipping duplicates.
4. For the remaining subarray, use two pointers (`left`, `right`) to find
   pairs summing to `target - nums[i] - nums[j]` — identical in spirit to
   the two-pointer core of 3Sum, just one level deeper.

**Pruning:** at both the `i` and `j` levels, two cheap checks skip whole
ranges of useless work:
- If the *smallest* possible sum using the current prefix (current
  element(s) plus the next smallest ones) already exceeds `target`, every
  larger choice at this level is hopeless too — `break` out entirely.
- If the *largest* possible sum using the current prefix (current
  element(s) plus the largest remaining ones) is still below `target`,
  this choice is too small — `continue` to the next one.

**Time:** O(n³) — O(n log n) sort, then O(n²) pairs of fixed elements
(`i`, `j`), each running an O(n) two-pointer scan.
**Space:** O(1) extra (excluding the output and the sort's own overhead).

### 2. `fourSumBruteForce` — check every quadruplet (for comparison)

Four nested loops over all `a < b < c < d`, collecting matches in a set
of sorted tuples to naturally deduplicate. Simple and clearly correct,
but far slower — used only to cross-check the two-pointer result in the
test suite.

**Time:** O(n⁴)
**Space:** O(n⁴) worst case for the dedup set (bounded in practice by the
actual number of valid quadruplets).

## Running

```bash
python3 solution.py
```

Runs a built-in test suite (including the problem's own examples,
all-equal and all-zero arrays, a larger array with many valid
quadruplets, and a case using values near the `10^9` bound to sanity
check for overflow-style issues — not a concern in Python, but worth
testing since this problem is a classic source of integer-overflow bugs
in other languages). Results are normalized (each quadruplet sorted, then
the list of quadruplets sorted) before comparing against expected output
and against the brute-force solution, with pass/fail printed per case.