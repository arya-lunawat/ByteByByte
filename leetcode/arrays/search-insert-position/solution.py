"""
LeetCode 35 - Search Insert Position
https://leetcode.com/problems/search-insert-position/

Given a sorted array of distinct integers and a target value, return
the index if the target is found. If not, return the index where it
would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Linear scan.

    Walk the array left to right and return the first index whose
    value is >= target -- that's exactly where target belongs, whether
    or not it's already present. If nothing qualifies, target is larger
    than everything, so it belongs at the very end.

    Time:  O(n)
    Space: O(1)
    """

    def searchInsert(self, nums: List[int], target: int) -> int:
        for i, val in enumerate(nums):
            if val >= target:
                return i
        return len(nums)


class Solution:
    """
    Approach: Binary search for the leftmost insertion point.

    This is really just binary search with a slightly different stop
    condition than "find an exact match". We narrow [low, high] until
    it collapses, at each step asking "could the target still be to
    the left of mid (inclusive), or does it have to be strictly to the
    right?":

      - If nums[mid] < target, target must be inserted somewhere after
        mid, so low = mid + 1.
      - Otherwise (nums[mid] >= target), mid is a valid candidate
        insertion point (either the match itself or a value target
        should be inserted before), so high = mid - 1 to keep looking
        for an even earlier valid spot.

    When the loop ends, `low` has converged to the correct insertion
    index -- if target exists in nums, low lands exactly on it (since
    nums has distinct values); if not, low lands where it should be
    inserted to keep the array sorted.

    Time:  O(log n)
    Space: O(1)
    """

    def searchInsert(self, nums: List[int], target: int) -> int:
        low, high = 0, len(nums) - 1

        while low <= high:
            mid = (low + high) // 2
            if nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        return low


if __name__ == "__main__":
    tests = [
        ([1, 3, 5, 6], 5, 2),
        ([1, 3, 5, 6], 2, 1),
        ([1, 3, 5, 6], 7, 4),
        ([1, 3, 5, 6], 0, 0),
        ([1], 1, 0),
        ([1, 3], 3, 1),
        ([1, 3, 5, 7, 9], 4, 2),
    ]

    for nums, target, expected in tests:
        r_brute = SolutionBruteForce().searchInsert(nums[:], target)
        r_opt = Solution().searchInsert(nums[:], target)
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"searchInsert({nums}, target={target}) -> "
            f"brute={r_brute} [{s_brute}], optimal={r_opt} [{s_opt}], expected={expected}"
        )