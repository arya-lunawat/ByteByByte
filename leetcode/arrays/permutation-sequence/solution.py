"""
LeetCode 46 - Permutations
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible
permutations. You can return the answer in any order.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Backtracking with a separate "used" boolean array and a
    freshly-copied path list appended at each leaf.

    At each recursive call, try every not-yet-used number as the next
    element of the current path: mark it used, append it to the path,
    recurse, then undo both (mark unused, pop) to try the next
    candidate. When the path length reaches n, a full permutation has
    been built -- copy it into the results.

    This is a completely standard, correct approach, but it carries
    the overhead of maintaining a separate `used` array (an extra O(n)
    structure alongside the path itself) and rescanning candidates
    from the full nums array every single call, rather than physically
    partitioning nums into "already placed" / "still available" the
    way the in-place swap approach does.

    Time:  O(n * n!) -- n! permutations, O(n) to copy each one (plus
           O(n) scanning overhead per call for the `used` checks).
    Space: O(n) for `used`, the recursion stack, and the path -- plus
           O(n * n!) for the output itself.
    """

    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        result: List[List[int]] = []
        path: List[int] = []
        used = [False] * n

        def backtrack() -> None:
            if len(path) == n:
                result.append(path[:])
                return

            for i in range(n):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return result


class Solution:
    """
    Approach: Backtracking via in-place swaps (no extra "used" array).

    Partition nums conceptually into two zones using a single pointer
    `start`: indices [0, start) hold the permutation prefix chosen so
    far, and indices [start, n) hold the values still available to
    place next. To choose the next element, swap it into position
    `start` (extending the "chosen" zone by one), recurse on the
    remainder, then swap back afterward to restore the array for the
    next sibling call (undoing the choice).

    This avoids the separate `used` array entirely -- "used" is
    implicitly encoded by living in the [0, start) prefix of the same
    array we're permuting, and choosing/un-choosing an element is a
    single O(1) swap rather than a used[i] = True/False bookkeeping
    step layered on top of a separate path list.

    When start == n, the array in its current arrangement IS a
    complete permutation, so we copy it directly into the results.

    Time:  O(n * n!) -- same asymptotic bound as brute force (n!
           permutations, O(n) to copy each), but with lower constant
           factor per call since there's no separate `used` array to
           maintain and no path-list append/pop bookkeeping -- just
           index swaps directly on nums.
    Space: O(n) for the recursion stack -- no extra `used` array or
           separate path list needed, since nums itself IS the
           in-progress permutation -- plus O(n * n!) for the output.
    """

    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        result: List[List[int]] = []

        def backtrack(start: int) -> None:
            if start == n:
                result.append(nums[:])
                return

            for i in range(start, n):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]  # swap back

        backtrack(0)
        return result


def normalize(perms: List[List[int]]) -> List[List[int]]:
    return sorted(perms)


if __name__ == "__main__":
    import math

    tests = [
        ([1, 2, 3], [
            [1, 2, 3], [1, 3, 2], [2, 1, 3],
            [2, 3, 1], [3, 1, 2], [3, 2, 1],
        ]),
        ([0, 1], [[0, 1], [1, 0]]),
        ([1], [[1]]),
        ([1, 2, 3, 4], None),  # just checking count/uniqueness below
    ]

    for nums, expected in tests:
        r_brute = normalize(SolutionBruteForce().permute(nums[:]))
        r_opt = normalize(Solution().permute(nums[:]))

        if expected is not None:
            exp = normalize(expected)
            s_brute = "PASS" if r_brute == exp else "FAIL"
            s_opt = "PASS" if r_opt == exp else "FAIL"
            print(
                f"permute({nums}) -> brute={r_brute} [{s_brute}], "
                f"optimal={r_opt} [{s_opt}], expected={exp}"
            )
        else:
            expected_count = math.factorial(len(nums))
            ok_brute = len(r_brute) == expected_count and len(set(map(tuple, r_brute))) == expected_count
            ok_opt = len(r_opt) == expected_count and len(set(map(tuple, r_opt))) == expected_count
            print(
                f"permute({nums}) -> brute count={len(r_brute)} "
                f"[{'PASS' if ok_brute else 'FAIL'}], "
                f"optimal count={len(r_opt)} [{'PASS' if ok_opt else 'FAIL'}], "
                f"expected count={expected_count} (all unique)"
            )