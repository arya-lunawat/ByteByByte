"""
55. Jump Game
https://leetcode.com/problems/jump-game/

You are given an integer array nums. You are initially positioned at
the array's first index, and each element in the array represents
your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.

Example:
    Input:  nums = [2,3,1,1,4]
    Output: true
    Explanation: Jump 1 step from index 0 to 1, then 3 steps to the
    last index.

    Input:  nums = [3,2,1,0,4]
    Output: false
    Explanation: You will always arrive at index 3 no matter what.
    Its maximum jump length is 0, which makes it impossible to reach
    the last index.

Constraints:
    1 <= nums.length <= 10^4
    0 <= nums[i] <= 10^5
"""

from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """
        Approach 1: Greedy, tracking the farthest reachable index.

        Scan left to right, maintaining `farthest`, the furthest index
        reachable using jumps decided so far. At each index i, if
        i > farthest, that index is unreachable, so the whole array is
        unreachable (return False immediately). Otherwise, update
        `farthest = max(farthest, i + nums[i])`. If `farthest` ever
        reaches or passes the last index, the answer is True -- no
        need to keep scanning.

        This works because we never need to know *which* sequence of
        jumps gets us to any given index, only *whether* some jump
        sequence can -- and the single "farthest reachable so far"
        value is exactly the information needed to answer that for
        every index in one pass.

        Time:  O(n) -- single left-to-right pass.
        Space: O(1) -- one running variable.
        """
        farthest = 0
        n = len(nums)
        for i in range(n):
            if i > farthest:
                return False
            farthest = max(farthest, i + nums[i])
            if farthest >= n - 1:
                return True
        return True

    def canJumpBackwards(self, nums: List[int]) -> bool:
        """
        Approach 2: Greedy, working backward from the goal.

        Start by treating the last index as the "goal" that must be
        reached. Scan from right to left: for every index i, if
        i + nums[i] reaches at least the current goal, then i itself
        becomes the new (easier) goal -- if you can get from i to the
        old goal, then reaching i is just as good as reaching the old
        goal directly. At the end, the goal has been "pulled" back to
        index 0 if and only if the last index was originally
        reachable from the start.

        Time:  O(n) -- single right-to-left pass.
        Space: O(1) -- one running variable (the current goal index).
        """
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([2, 3, 1, 1, 4], True),
        ([3, 2, 1, 0, 4], False),
        ([0], True),
        ([1, 0, 1, 0], False),
        ([2, 0, 0], True),
        ([0, 1], False),
        ([1, 1, 1, 1], True),
        ([5, 0, 0, 0, 0, 0], True),
        ([1, 2, 0, 1, 0, 1, 0], False),
        ([2, 5, 0, 0], True),
    ]

    methods = [
        ("canJump (forward greedy, farthest reachable)", solution.canJump),
        ("canJumpBackwards (backward greedy, shrinking goal)", solution.canJumpBackwards),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (nums, expected) in enumerate(test_cases, 1):
            actual = method(nums[:])
            assert actual == expected, (
                f"Test {i} FAILED for {name}: nums={nums}\n"
                f"  expected={expected}, actual={actual}"
            )
            print(f"  Test {i} passed: nums={nums} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()