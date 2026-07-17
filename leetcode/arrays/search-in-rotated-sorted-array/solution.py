"""
LeetCode 33 - Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

There is an integer array nums sorted in ascending order (with distinct
values). Prior to being passed to your function, nums is possibly
rotated at an unknown pivot index k such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]].

Given nums after the possible rotation and an integer target, return
the index of target if it is in nums, or -1 if it is not.

You must write an algorithm with O(log n) runtime complexity.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Linear scan.

    Completely ignores the sorted-and-rotated structure and just checks
    every element. Correct, but doesn't meet the problem's required
    O(log n) runtime.

    Time:  O(n)
    Space: O(1)
    """

    def search(self, nums: List[int], target: int) -> int:
        for i, val in enumerate(nums):
            if val == target:
                return i
        return -1


class Solution:
    """
    Approach: Modified binary search.

    A rotated sorted array is really two sorted halves glued together.
    At any [low, high] window, at least one of the two halves split by
    `mid` is guaranteed to be fully sorted -- so on every iteration we
    can identify the sorted half, check whether target falls inside
    its range, and discard the other half accordingly:

      1. If nums[mid] == target, we're done.
      2. If nums[low] <= nums[mid], the LEFT half [low, mid] is sorted.
         - If target is within [nums[low], nums[mid]), search left.
         - Otherwise, search right.
      3. Otherwise, the RIGHT half [mid, high] is sorted.
         - If target is within (nums[mid], nums[high]], search right.
         - Otherwise, search left.

    Each step throws away roughly half the search space, same as
    standard binary search, just with an extra check to figure out
    which half is safe to reason about.

    Time:  O(log n)
    Space: O(1)
    """

    def search(self, nums: List[int], target: int) -> int:
        low, high = 0, len(nums) - 1

        while low <= high:
            mid = (low + high) // 2

            if nums[mid] == target:
                return mid

            if nums[low] <= nums[mid]:
                # Left half [low, mid] is sorted.
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                # Right half [mid, high] is sorted.
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1

        return -1


if __name__ == "__main__":
    tests = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([1], 1, 0),
        ([5, 1, 3], 5, 0),
        ([3, 1], 1, 1),
        ([1, 2, 3, 4, 5], 3, 2),  # no rotation
        ([6, 7, 0, 1, 2, 4, 5], 6, 0),
        ([6, 7, 0, 1, 2, 4, 5], 5, 6),
    ]

    for nums, target, expected in tests:
        r_brute = SolutionBruteForce().search(nums[:], target)
        r_opt = Solution().search(nums[:], target)
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"search({nums}, target={target}) -> "
            f"brute={r_brute} [{s_brute}], optimal={r_opt} [{s_opt}], expected={expected}"
        )