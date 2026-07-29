# 46. Permutations

[LeetCode Problem](https://leetcode.com/problems/permutations/)

## Problem

Given an array `nums` of distinct integers, return **all** possible
permutations, in any order.

```
Input:  nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Constraints**
- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All integers in `nums` are unique.

## Approaches

### 1. Backtracking with in-place swap — `permute()`

Fix the element at index `start` by trying every candidate from `start`
to the end, swapping it into place, recursing on `start + 1`, then
swapping back to restore the array before trying the next candidate.
When `start` reaches `n`, `nums` holds one full permutation, which gets
copied into the result.

- **Time:** `O(n · n!)` — there are `n!` permutations, and each costs
  `O(n)` to copy into the result.
- **Space:** `O(n)` recursion depth, not counting the output. No extra
  arrays needed since the swapping happens in place.

This is the standard, most memory-efficient backtracking solution.

### 2. Iterative build-up by insertion — `permuteBuildUp()`

Start from the trivial set of permutations of the empty list, `[[]]`.
For each number in `nums`, generate the next generation of permutations
by inserting that number into every gap (before, between, and after the
existing elements) of every permutation built so far.

- **Time:** `O(n · n!)`
- **Space:** `O(n · n!)` — every intermediate generation of permutations
  is stored, not just the recursion stack.

No recursion at all, which can be easier to reason about, at the cost
of holding onto more intermediate lists.

### 3. Backtracking with a `used[]` tracker — `permuteUsedSet()`

Functionally the same idea as approach 1, but instead of swapping
elements in place, it keeps a separate `path` list for the permutation
being built and a `used` boolean array to mark which indices have
already been placed. Arguably the most readable version, at the cost
of an extra `O(n)` array.

- **Time:** `O(n · n!)`
- **Space:** `O(n)` for `used` and `path`, not counting the output.

## Testing

`solution.py` runs all three approaches against 8 test cases, including
duplicates-of-signed-numbers and single-element inputs. Each result is
checked for:

- the correct count (`n!` permutations),
- no duplicate permutations,
- every output being a valid rearrangement of the input,
- and, where a known answer is provided, an exact (order-independent)
  match.

```
python3 solution.py
```

All test cases pass for all three implementations.