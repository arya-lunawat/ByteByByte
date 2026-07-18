"""
LeetCode 40 - Combination Sum II
https://leetcode.com/problems/combination-sum-ii/

Given a collection of candidate numbers (candidates, which MAY contain
duplicates) and a target number (target), find all unique combinations
in candidates where the candidate numbers sum to target.

Each number in candidates may only be used ONCE in each combination.

Note: The solution set must not contain duplicate combinations.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Backtrack without duplicate-awareness, dedupe afterward.

    Sort candidates (needed only so combinations come out in a
    consistent, comparable order) and run plain "0/1 knapsack"-style
    backtracking: at each step, either skip a candidate or take it and
    move strictly forward (i + 1, since each element can be used at
    most once). This explores every possible subset-sum combination,
    including ones that are identical in value but built from
    different duplicate copies of the same number (e.g. picking "the
    first 1" vs "the second 1" when candidates has two 1's) -- these
    show up as separate branches in the search tree even though they
    produce the same output list.

    To get a duplicate-free answer, every raw combination found is
    converted to a tuple and stuffed into a set, discarding true
    duplicates only after they've already been fully generated. This
    wastes work re-exploring and re-recording combinations that a
    duplicate-aware version would have skipped before ever recursing.

    Time:  Same exponential search space as the optimal version, but
           without early duplicate-skipping, so more (redundant)
           branches are explored and later thrown away during dedup.
    Space: O(number of raw combinations before dedup), which can be
           significantly larger than the deduped result set.
    """

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates = sorted(candidates)
        raw_results: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                raw_results.append(path[:])
                return
            if remaining < 0 or start == len(candidates):
                return

            for i in range(start, len(candidates)):
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])  # each index used once
                path.pop()

        backtrack(0, target)

        seen = set()
        deduped: List[List[int]] = []
        for combo in raw_results:
            key = tuple(combo)
            if key not in seen:
                seen.add(key)
                deduped.append(combo)
        return deduped


class Solution:
    """
    Approach: Backtracking with sorted candidates + same-level dedup skip.

    Sort candidates first so identical values sit next to each other.
    While iterating over candidates at a given recursion depth (a
    single "level" of the search tree), skip any candidate that's the
    same value as the one immediately before it *at that same level*
    (i.e. `i > start and candidates[i] == candidates[i - 1]`).

    Why this works: within one level, taking the first occurrence of a
    duplicate value already explores every combination that using that
    value could produce (via its own recursive subtree, which considers
    all remaining later copies). Taking a second, third, etc. copy of
    the same value *at the same level* would just re-explore the exact
    same subtree again -- so skipping it prevents duplicate
    combinations from ever being generated in the first place, rather
    than filtering them out after the fact.

    Also prunes early: since candidates are sorted, if
    candidates[i] > remaining we can `break` immediately (every later
    candidate is even bigger).

    Time:  Same exponential search space in the worst case, but the
           same-level duplicate skip plus early break prunes a large
           fraction of redundant branches before recursing, so no
           post-hoc deduplication is needed and no wasted work is done
           generating combinations that would just be discarded.
    Space: O(number of unique combinations) for the output, plus
           O(target / min_candidate) recursion depth.
    """

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates = sorted(candidates)
        result: List[List[int]] = []
        path: List[int] = []
        n = len(candidates)

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, n):
                if candidates[i] > remaining:
                    break  # sorted -> nothing later can fit either

                if i > start and candidates[i] == candidates[i - 1]:
                    continue  # skip duplicate value at this level

                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])  # each index used once
                path.pop()

        backtrack(0, target)
        return result


def normalize(combos: List[List[int]]) -> List[List[int]]:
    return sorted(sorted(c) for c in combos)


if __name__ == "__main__":
    tests = [
        (
            [10, 1, 2, 7, 6, 1, 5],
            8,
            [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]],
        ),
        (
            [2, 5, 2, 1, 2],
            5,
            [[1, 2, 2], [5]],
        ),
        ([1], 2, []),
        ([1, 1], 2, [[1, 1]]),
        ([1, 1, 1], 1, [[1]]),
    ]

    for candidates, target, expected in tests:
        r_brute = normalize(SolutionBruteForce().combinationSum2(candidates, target))
        r_opt = normalize(Solution().combinationSum2(candidates, target))
        exp = normalize(expected)
        s_brute = "PASS" if r_brute == exp else "FAIL"
        s_opt = "PASS" if r_opt == exp else "FAIL"
        print(
            f"combinationSum2({candidates}, {target}) -> "
            f"brute={r_brute} [{s_brute}], optimal={r_opt} [{s_opt}], expected={exp}"
        )