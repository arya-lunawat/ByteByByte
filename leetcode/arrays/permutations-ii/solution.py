"""
47. Permutations II
https://leetcode.com/problems/permutations-ii/

Given a collection of numbers, nums, that might contain duplicates,
return all possible unique permutations in any order.

Example:
    Input:  nums = [1,1,2]
    Output: [[1,1,2],[1,2,1],[2,1,1]]

Constraints:
    1 <= nums.length <= 8
    -10 <= nums[i] <= 10
"""

from typing import List
from collections import Counter


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 1: Backtracking with sort + "skip the duplicate" rule.

        Sort nums first so that equal values sit next to each other.
        Track which indices are used with a `used[]` array. At each
        recursive step, skip a candidate i if:
          - it's already used, or
          - it's equal to nums[i-1] AND nums[i-1] hasn't been used yet
            in the current path.

        That second condition is the key trick: among a run of equal
        values, it forces them to always be placed in the *same
        relative order* they appear in the sorted array, which is
        exactly what prevents duplicate permutations from ever being
        generated (rather than generating and filtering them after).

        Time:  O(n * n!) -- same asymptotic count of permutations as
               the distinct-elements case, just without the duplicates;
               each valid permutation costs O(n) to copy out.
        Space: O(n) for `used` and the recursion stack, excluding output.
        """
        nums.sort()
        n = len(nums)
        result = []
        used = [False] * n
        path: List[int] = []

        def backtrack() -> None:
            if len(path) == n:
                result.append(path[:])
                return
            for i in range(n):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return result

    def permuteUniqueCounter(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 2: Backtracking driven by a value -> count map.

        Instead of tracking *which indices* are used, track how many
        copies of each *distinct value* remain available. At each
        step, try every distinct value that still has count > 0,
        decrement it, recurse, then restore it. Since we branch on
        distinct values rather than indices, duplicate permutations
        are never produced in the first place -- no extra
        skip-condition bookkeeping needed.

        Time:  O(n * n!)
        Space: O(k) for the counter (k = number of distinct values),
               plus O(n) recursion stack / path, excluding output.
        """
        n = len(nums)
        counts = Counter(nums)
        result = []
        path: List[int] = []

        def backtrack() -> None:
            if len(path) == n:
                result.append(path[:])
                return
            for value in counts:
                if counts[value] == 0:
                    continue
                counts[value] -= 1
                path.append(value)
                backtrack()
                path.pop()
                counts[value] += 1

        backtrack()
        return result


def _normalize(perms: List[List[int]]):
    return sorted(tuple(p) for p in perms)


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
        ([1, 2, 3], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
        ([1], [[1]]),
        ([2, 2], [[2, 2]]),
        ([1, 1, 1], [[1, 1, 1]]),
        ([0, -1, 0], [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]),
        ([1, 1, 2, 2], None),  # checked structurally below
        ([5, 5, 5, 6, 6], None),
    ]

    def unique_permutation_count(nums: List[int]) -> int:
        from math import factorial
        counts = Counter(nums)
        total = factorial(len(nums))
        for c in counts.values():
            total //= factorial(c)
        return total

    methods = [
        ("permuteUnique (sort + skip-duplicate)", solution.permuteUnique),
        ("permuteUniqueCounter (value counts)", solution.permuteUniqueCounter),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (nums, expected) in enumerate(test_cases, 1):
            actual = method(nums[:])

            normalized = _normalize(actual)
            assert len(normalized) == len(actual), (
                f"Test {i} FAILED for {name}: duplicate permutations produced "
                f"for nums={nums}"
            )

            expected_count = unique_permutation_count(nums)
            assert len(actual) == expected_count, (
                f"Test {i} FAILED for {name}: expected {expected_count} unique "
                f"permutations for nums={nums}, got {len(actual)}"
            )

            for perm in actual:
                assert sorted(perm) == sorted(nums), (
                    f"Test {i} FAILED for {name}: {perm} is not a permutation of {nums}"
                )

            if expected is not None:
                assert normalized == _normalize(expected), (
                    f"Test {i} FAILED for {name}: nums={nums}\n"
                    f"  expected={expected}\n  actual={actual}"
                )

            print(f"  Test {i} passed: nums={nums} -> {len(actual)} unique permutations")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()