"""
LeetCode 34 - Find First and Last Position of Element in Sorted Array
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

Given an array of integers nums sorted in non-decreasing order, find the
starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Linear scan.

    Walk the array once, remembering the first index where nums[i] ==
    target and the last index where that's true. Correct, but doesn't
    meet the required O(log n) runtime -- included as a baseline.

    Time:  O(n)
    Space: O(1)
    """

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        first = -1
        last = -1
        for i, val in enumerate(nums):
            if val == target:
                if first == -1:
                    first = i
                last = i
        return [first, last]


class Solution:
    """
    Approach: Two binary searches (leftmost / rightmost bound).

    Standard binary search only tells you *that* a target exists, not
    the extent of its run when duplicates are present. The fix: run
    binary search twice with a small tweak each time, both O(log n):

      - find_bound(target, find_first=True): whenever nums[mid] ==
        target, don't stop -- record mid as a candidate and keep
        searching the LEFT half (high = mid - 1) to see if an earlier
        occurrence exists.
      - find_bound(target, find_first=False): symmetric, but keep
        searching the RIGHT half (low = mid + 1) to push the candidate
        as late as possible.

    In both cases, if nums[mid] < target we move low = mid + 1, and if
    nums[mid] > target we move high = mid - 1, exactly like normal
    binary search -- only the "found" branch's direction changes.

    Time:  O(log n) -- two independent binary searches
    Space: O(1)
    """

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        first = self._find_bound(nums, target, find_first=True)
        if first == -1:
            return [-1, -1]
        last = self._find_bound(nums, target, find_first=False)
        return [first, last]

    def _find_bound(self, nums: List[int], target: int, find_first: bool) -> int:
        low, high = 0, len(nums) - 1
        result = -1

        while low <= high:
            mid = (low + high) // 2

            if nums[mid] < target:
                low = mid + 1
            elif nums[mid] > target:
                high = mid - 1
            else:
                result = mid
                if find_first:
                    high = mid - 1  # keep looking left for an earlier match
                else:
                    low = mid + 1   # keep looking right for a later match

        return result


if __name__ == "__main__":
    tests = [
        ([5, 7, 7, 8, 8, 10], 8, [3, 4]),
        ([5, 7, 7, 8, 8, 10], 6, [-1, -1]),
        ([], 0, [-1, -1]),
        ([1], 1, [0, 0]),
        ([2, 2], 2, [0, 1]),
        ([1, 2, 3, 4, 5], 1, [0, 0]),
        ([1, 2, 3, 4, 5], 5, [4, 4]),
        ([1, 1, 1, 1, 1], 1, [0, 4]),
    ]

    for nums, target, expected in tests:
        r_brute = SolutionBruteForce().searchRange(nums[:], target)
        r_opt = Solution().searchRange(nums[:], target)
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"searchRange({nums}, target={target}) -> "
            f"brute={r_brute} [{s_brute}], optimal={r_opt} [{s_opt}], expected={expected}"
        )