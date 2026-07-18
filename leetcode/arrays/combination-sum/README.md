# 39. Combination Sum

**Difficulty:** Medium
**Link:** https://leetcode.com/problems/combination-sum/
**Topics:** Array, Backtracking

## Problem

Given an array of **distinct** integers `candidates` and a target
integer `target`, return a list of all **unique combinations** of
`candidates` where the chosen numbers sum to `target`. You may return
the combinations in any order.

The **same number may be chosen from `candidates` an unlimited number
of times**. Two combinations are unique if the frequency of at least
one of the chosen numbers is different.

It is guaranteed that the number of unique combinations that sum up to
`target` is fewer than 150 for the given input.

### Examples

```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]

Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Input: candidates = [2], target = 1
Output: []
```

### Constraints

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All elements of `candidates` are **distinct**.
- `1 <= target <= 40`

## Approach 1: Backtracking Without Pruning

At each step, try every candidate starting from the current index
(reusing the same index forward, not `i + 1`, since a number can be
picked more than once — but never looking backward, which avoids
generating the same combination in a different order). Subtract the
chosen candidate from the remaining target and recurse. A branch ends
when the remaining target hits exactly `0` (record the combination) or
drops below `0` (dead end).

Because candidates are tried in their **original, unsorted** order, we
can't safely stop scanning early just because one candidate overshoots
the remaining target — a smaller candidate might still appear later in
the list. So every branch gets attempted, and overshoots are only
discovered one recursion level down via the `remaining < 0` check.

- **Time:** Roughly `O(k^(T/m))` (`k` = number of candidates, `T` =
  target, `m` = the smallest candidate value) — exponential, and here
  made worse in practice by exploring extra dead branches before
  failing.
- **Space:** `O(T/m)` recursion depth, plus `O(number of combinations)`
  for the output.

## Approach 2: Backtracking with Sorted Candidates + Early Pruning (Optimal)

Sort `candidates` first. Now, while trying candidates at each step in
ascending order, the moment a candidate **exceeds** the remaining
target we can `break` out of the loop immediately — since the list is
sorted, every candidate after it is even larger and would overshoot
too. This prunes entire subtrees of the search space *before* ever
recursing into them, rather than discovering the overshoot a level
deeper.

- **Time:** Same worst-case asymptotic bound as the brute-force
  version (`O(k^(T/m))`) — this is inherently a combinatorial search
  problem — but the sorted-order early break prunes a large fraction
  of the search tree in practice, giving a meaningful real-world
  speedup.
- **Space:** `O(T/m)` recursion depth, plus `O(number of combinations)`
  for the output.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard examples, a case with no valid combinations,
  and small single-candidate edge cases.

## Complexity Summary

| Approach                                | Time         | Space |
|--------------------------------------------|--------------|-------|
| Backtracking, unsorted (no early pruning)   | O(k^(T/m))   | O(T/m) |
| Backtracking, sorted + early break (optimal) | O(k^(T/m))  | O(T/m) |

*(k = number of candidates, T = target, m = smallest candidate value — same asymptotic bound, but the optimal version prunes far more branches in practice.)*