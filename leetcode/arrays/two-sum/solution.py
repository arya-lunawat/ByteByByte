"""
LeetCode 1: Two Sum
https://leetcode.com/problems/two-sum/

Given an array of integers `nums` and an integer `target`, return the
indices of the two numbers such that they add up to `target`.

Assumptions:
- Exactly one valid answer exists.
- The same element cannot be used twice.
"""

from typing import List


def two_sum_brute_force(nums: List[int], target: int) -> List[int]:
    """
    Check every pair of elements.

    Time:  O(n^2) - nested loop over all pairs
    Space: O(1)   - no extra data structures
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def two_sum_optimal(nums: List[int], target: int) -> List[int]:
    """
    Single pass using a hash map.

    For each value, check whether its complement (target - value) has
    already been seen. If so, we've found our pair. Otherwise, record
    the current value's index and keep going.

    Time:  O(n) - one pass through the array, O(1) average dict lookups
    Space: O(n) - hash map can hold up to n elements
    """
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9

    print("Brute force:", two_sum_brute_force(nums, target))  # [0, 1]
    print("Optimal:     ", two_sum_optimal(nums, target))      # [0, 1]
