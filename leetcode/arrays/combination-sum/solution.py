"""
LeetCode 39 - Combination Sum
https://leetcode.com/problems/combination-sum/

Given an array of distinct integers `candidates` and a target integer
`target`, return a list of all unique combinations of candidates where
the chosen numbers sum to target. You may return the combinations in
any order.

The same number may be chosen from candidates an unlimited number of
times. Two combinations are unique if the frequency of at least one of
the chosen numbers is different.

It is guaranteed that the number of unique combinations that sum up to
target is less than 150 combinations for the given input.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Backtracking without sorting or early pruning.

    At each step, try every candidate (starting from the current index
    to avoid generating permutations of the same combination), subtract
    it from the remaining target, and recurse. Stop a branch when the
    remaining target hits exactly 0 (record the combination) or drops
    below 0 (dead end -- but we don't discover this until *after*
    recursing one level deeper and checking, since candidates aren't
    sorted and we can't safely break early).

    Because candidates are visited in their original (unsorted) order,
    we can't stop scanning early just because one candidate overshoots
    the remaining target -- a later, smaller candidate might still
    work. So every branch has to be attempted and only cut off via the
    `remaining < 0` base case one level down.

    Time:  O(k^(T/m)) roughly, where k = len(candidates), T = target,
           m = minimum candidate value -- exponential, and here made
           worse in practice by not pruning based on sorted order, so
           more dead branches are explored before failing.
    Space: O(T/m) for recursion depth, plus O(number of combinations)
           for the output.
    """

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return
            if remaining < 0:
                return

            for i in range(start, len(candidates)):
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i])  # reuse allowed -> i, not i+1
                path.pop()

        backtrack(0, target)
        return result


class Solution:
    """
    Approach: Backtracking with sorted candidates + early pruning.

    Sort `candidates` first. Then, while trying candidates at each
    step in ascending order, the moment a candidate exceeds the
    remaining target we can `break` out of the loop entirely --
    every candidate after it (being even larger, since the list is
    sorted) would overshoot too, so there's no need to even consider
    them. This prunes whole subtrees of the search space before ever
    recursing into them, unlike the brute-force version which only
    discovers the overshoot one level deeper.

    Time:  O(k^(T/m)) in the worst case (same asymptotic bound as the
           brute-force version -- this is fundamentally a combinatorial
           search problem), but the sorted-order early break prunes a
           large fraction of the search tree in practice, making it
           meaningfully faster on real inputs.
    Space: O(T/m) for recursion depth, plus O(number of combinations)
           for the output.
    """

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates = sorted(candidates)
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break  # sorted -> everything after is even bigger, stop early

                path.append(candidates[i])
                backtrack(i, remaining - candidates[i])  # reuse allowed -> i, not i+1
                path.pop()

        backtrack(0, target)
        return result


def normalize(combos: List[List[int]]) -> List[List[int]]:
    return sorted(sorted(c) for c in combos)


if __name__ == "__main__":
    tests = [
        ([2, 3, 6, 7], 7, [[2, 2, 3], [7]]),
        ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
        ([2], 1, []),
        ([1], 1, [[1]]),
        ([1], 2, [[1, 1]]),
    ]

    for candidates, target, expected in tests:
        r_brute = normalize(SolutionBruteForce().combinationSum(candidates, target))
        r_opt = normalize(Solution().combinationSum(candidates, target))
        exp = normalize(expected)
        s_brute = "PASS" if r_brute == exp else "FAIL"
        s_opt = "PASS" if r_opt == exp else "FAIL"
        print(
            f"combinationSum({candidates}, {target}) -> "
            f"brute={r_brute} [{s_brute}], optimal={r_opt} [{s_opt}], expected={exp}"
        )