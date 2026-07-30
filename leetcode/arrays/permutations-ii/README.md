# 47. Permutations II

[LeetCode Problem](https://leetcode.com/problems/permutations-ii/)

## Problem

Given a collection of numbers, `nums`, that might contain duplicates,
return all possible **unique** permutations, in any order.

```
Input:  nums = [1,1,2]
Output: [[1,1,2],[1,2,1],[2,1,1]]
```

**Constraints**
- `1 <= nums.length <= 8`
- `-10 <= nums[i] <= 10`

The twist versus [Permutations (46)](../46-permutations/): duplicate
values in the input must not produce duplicate permutations in the
output. The naive fix — generate everything and dedupe with a `set` —
wastes exponential work generating permutations you then throw away.
Both approaches below avoid ever generating a duplicate in the first
place.

## Approaches

### 1. Sort + "skip the duplicate" backtracking — `permuteUnique()`

Sort `nums` so equal values are adjacent, then backtrack over
*indices* with a `used[]` array, same shape as the classic
Permutations solution. The one addition: skip index `i` if
`nums[i] == nums[i-1]` and `nums[i-1]` is **not** currently used.

That condition forces equal values to always be placed in the same
relative order they appear in the sorted array. Any permutation that
would place a "later" duplicate before an unused "earlier" one is
exactly the kind of arrangement that's indistinguishable from one
already produced — so it's pruned before it's ever built, rather than
filtered out afterward.

- **Time:** `O(n · n!)` — bounded by the (now smaller) count of unique
  permutations, each costing `O(n)` to copy out.
- **Space:** `O(n)` for `used` and the recursion stack, excluding output.

### 2. Value-count backtracking — `permuteUniqueCounter()`

Instead of tracking which *indices* have been used, track how many
copies of each *distinct value* remain (`Counter`). At each step,
branch on every distinct value with a remaining count greater than
zero, decrement it, recurse, then restore it.

Because branching happens over distinct values rather than indices,
there's no way to ever place "the first 1" and "the second 1" in a
way that produces two different-looking-but-identical permutations —
the bookkeeping problem doesn't exist rather than needing a rule to
avoid it. Arguably the more natural formulation once duplicates are in
play.

- **Time:** `O(n · n!)`
- **Space:** `O(k)` for the counter (`k` = distinct values), plus
  `O(n)` for the path/recursion stack, excluding output.

## Testing

`solution.py` runs both approaches against 8 test cases, including
all-duplicate inputs (`[2,2]`, `[1,1,1]`), mixed-duplicate inputs
(`[1,1,2,2]`, `[5,5,5,6,6]`), negatives, and single elements. Each
result is checked for:

- the correct count of *unique* permutations (computed as
  `n! / (c1! · c2! · ...)` for duplicate-value counts `c1, c2, ...`),
- no duplicate permutations in the output,
- every output being a valid rearrangement of the input,
- and, where a known answer is provided, an exact (order-independent)
  match.

```
python3 solution.py
```

All test cases pass for both implementations.