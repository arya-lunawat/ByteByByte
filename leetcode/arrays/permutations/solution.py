"""
46. Permutations
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible
permutations. You can return the answer in any order.

Example:
    Input:  nums = [1,2,3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Constraints:
    1 <= nums.length <= 6
    -10 <= nums[i] <= 10
    All integers in nums are unique.
"""

from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 1: Backtracking with an in-place swap.

        At each recursion depth `start`, every index from `start` onward
        gets a turn being swapped into position `start`. Once `start`
        reaches the end of the array, the current arrangement is a
        complete permutation.

        Time:  O(n * n!)  -- n! permutations, O(n) to copy each one
        Space: O(n) recursion depth (excluding the output)
        """
        result = []
        n = len(nums)

        def backtrack(start: int) -> None:
            if start == n:
                result.append(nums[:])
                return
            for i in range(start, n):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]  # undo

        backtrack(0)
        return result

    def permuteBuildUp(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 2: Iterative build-up by insertion.

        Start with the permutations of an empty list ([[]]) and, for each
        new number, insert it into every possible position of every
        permutation built so far.

        Time:  O(n * n!)
        Space: O(n * n!) for the growing list of permutations
        """
        permutations: List[List[int]] = [[]]
        for num in nums:
            next_permutations = []
            for perm in permutations:
                for i in range(len(perm) + 1):
                    next_permutations.append(perm[:i] + [num] + perm[i:])
            permutations = next_permutations
        return permutations

    def permuteUsedSet(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 3: Backtracking with an explicit "used" tracker and a
        separate path list, instead of swapping in place. Slightly more
        intuitive to read, at the cost of an extra boolean array.

        Time:  O(n * n!)
        Space: O(n) for `used` and `path` (excluding the output)
        """
        result = []
        n = len(nums)
        used = [False] * n
        path: List[int] = []

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


def _normalize(perms: List[List[int]]):
    return sorted(tuple(p) for p in perms)


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([1, 2, 3], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
        ([0, 1], [[0, 1], [1, 0]]),
        ([1], [[1]]),
        ([1, 2], [[1, 2], [2, 1]]),
        ([-1, 0, 1], [[-1, 0, 1], [-1, 1, 0], [0, -1, 1], [0, 1, -1], [1, -1, 0], [1, 0, -1]]),
        ([5, 4, 3, 2], None),   # None => just check count/shape, not exact contents below
        ([1, 2, 3, 4], None),
        ([9, -9], [[9, -9], [-9, 9]]),
    ]

    methods = [
        ("permute (swap backtracking)", solution.permute),
        ("permuteBuildUp (insertion)", solution.permuteBuildUp),
        ("permuteUsedSet (used[] backtracking)", solution.permuteUsedSet),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (nums, expected) in enumerate(test_cases, 1):
            actual = method(nums[:])  # copy, since permute() mutates nums

            # Structural checks that always apply.
            assert len(actual) == len(set(_normalize(actual))), (
                f"Test {i} FAILED for {name}: duplicate permutations produced"
            )
            from math import factorial
            assert len(actual) == factorial(len(nums)), (
                f"Test {i} FAILED for {name}: expected {factorial(len(nums))} "
                f"permutations, got {len(actual)}"
            )
            for perm in actual:
                assert sorted(perm) == sorted(nums), (
                    f"Test {i} FAILED for {name}: {perm} is not a permutation of {nums}"
                )

            if expected is not None:
                assert _normalize(actual) == _normalize(expected), (
                    f"Test {i} FAILED for {name}: nums={nums}\n"
                    f"  expected={expected}\n  actual={actual}"
                )

            print(f"  Test {i} passed: nums={nums} -> {len(actual)} permutations")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()