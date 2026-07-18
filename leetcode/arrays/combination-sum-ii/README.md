# 40. Combination Sum II

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/combination-sum-ii/
**Topics:** Array, Backtracking

## Problem

Given a collection of candidate numbers `candidates` (which **may
contain duplicates**) and a target number `target`, find all unique
combinations in `candidates` where the numbers sum to `target`.

Each number in `candidates` may only be used **once** in each
combination.

> **Note:** The solution set must not contain duplicate combinations.

### Examples

```
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

Input: candidates = [2,5,2,1,2], target = 5
Output: [[1,2,2],[5]]
```

### Constraints

- `1 <= candidates.length <= 100`
- `1 <= candidates[i] <= 50`
- `1 <= target <= 30`

## Approach 1: Backtrack, Then Dedupe Afterward

Sort `candidates` (just to make combinations comparable) and run plain
"0/1 knapsack"-style backtracking: at each step, either take the
current candidate and move strictly forward (`i + 1`, since each
element index can be used at most once) or skip it. This explores
every subset-sum combination — including ones that are value-identical
but built from different duplicate *copies* of the same number (e.g.
picking "the first 1" vs. "the second 1" when `candidates` has two
1's). Those show up as separate branches in the search tree even
though they'd produce the same output list.

To get a duplicate-free answer, every raw combination is converted to
a tuple and pushed into a set, discarding true duplicates only **after
they've already been fully generated**. This wastes work exploring and
recording combinations that a duplicate-aware version would have
skipped before ever recursing into them.

- **Time:** Same exponential search space as the optimal version, but
  without early duplicate-skipping — more redundant branches get
  explored and thrown away during the post-hoc dedup pass.
- **Space:** `O(number of raw combinations before dedup)`, which can
  be noticeably larger than the final deduped result set.

## Approach 2: Sorted Candidates + Same-Level Duplicate Skip (Optimal)

Sort `candidates` first so identical values sit next to each other.
While iterating candidates at a given recursion depth (one "level" of
the search tree), **skip any candidate equal to the one immediately
before it at that same level**:
`if i > start and candidates[i] == candidates[i - 1]: continue`.

**Why this works:** within one level, taking the *first* occurrence of
a duplicate value already explores every combination that value could
possibly produce — its own recursive subtree considers all remaining
later copies. Taking a *second* copy of the same value at the *same*
level would just re-explore that exact same subtree again. Skipping it
prevents duplicate combinations from ever being generated at all,
rather than filtering them out afterward.

Also prunes early: since `candidates` is sorted, once
`candidates[i] > remaining`, every later candidate is even bigger, so
we can `break` out of the loop immediately.

- **Time:** Same exponential search space in the worst case, but the
  same-level duplicate skip plus early break prunes a large fraction
  of redundant branches *before* recursing — no post-hoc
  deduplication needed, and no wasted work generating combinations
  that would just be discarded.
- **Space:** `O(number of unique combinations)` for the output, plus
  `O(target / min_candidate)` recursion depth.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard examples, a case with no valid combinations,
  and small duplicate-heavy edge cases.

## Complexity Summary

| Approach                                     | Time       | Space |
|---------------------------------------------------|------------|-------|
| Backtrack + dedupe afterward                        | exponential (extra redundant branches) | O(raw combinations) |
| Sorted + same-level skip + early break (optimal)    | exponential (heavily pruned) | O(unique combinations) |