"""
LeetCode 16 - 3Sum Closest
https://leetcode.com/problems/3sum-closest/

Given an integer array nums of length n and an integer target, find
three integers in nums such that the sum is closest to target.

Return the sum of the three integers.

You may assume that each input would have exactly one solution.

Example 1:
    Input: nums = [-1,2,1,-4], target = 1
    Output: 2
    Explanation: The sum that is closest to the target is
    -1 + 2 + 1 = 2.

Example 2:
    Input: nums = [0,0,0], target = 1
    Output: 0
    Explanation: The sum that is closest to the target is
    0 + 0 + 0 = 0.

Constraints:
    3 <= nums.length <= 500
    -1000 <= nums[i] <= 1000
    -10^4 <= target <= 10^4
"""


class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        """
        Sort + two pointers (same skeleton as 3Sum, adapted to track the
        closest sum instead of exact zero-sum matches).

        Sort the array, fix one element at a time, and use two pointers
        on the rest to search for a sum near `target`. Every triplet sum
        we compute is compared to the best one found so far; if it's an
        exact match we can return immediately since nothing can beat a
        distance of 0.

        Time Complexity:  O(n^2) - O(n log n) sort + O(n) fixed elements
                           each doing an O(n) two-pointer scan
        Space Complexity: O(1) extra (excluding the sort's own overhead)
        """
        nums.sort()
        n = len(nums)
        closest_sum = nums[0] + nums[1] + nums[2]  # any valid starting guess

        for i in range(n - 2):
            # Skip duplicate fixed elements; doesn't change correctness,
            # just avoids redundant identical work.
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum

                if current_sum == target:
                    return current_sum  # can't get closer than exact
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return closest_sum

    def threeSumClosestBruteForce(self, nums: list[int], target: int) -> int:
        """
        Brute-force O(n^3) solution, provided for comparison: check every
        triplet directly.

        Time Complexity:  O(n^3)
        Space Complexity: O(1)
        """
        n = len(nums)
        closest_sum = nums[0] + nums[1] + nums[2]

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    current_sum = nums[i] + nums[j] + nums[k]
                    if abs(current_sum - target) < abs(closest_sum - target):
                        closest_sum = current_sum

        return closest_sum


def run_tests():
    sol = Solution()
    test_cases = [
        ([-1, 2, 1, -4], 1, 2),
        ([0, 0, 0], 1, 0),
        ([1, 1, 1, 0], -100, 2),
        ([1, 1, 1, 1], 0, 3),
        ([-3, -2, -5, 3, -4], -1, -2),
        ([4, 0, 5, -5, 3, 3, 0, -4, -5], -2, -2),
        ([1, 2, 5, 10, 11], 12, 13),
    ]

    all_passed = True
    for nums, target, expected in test_cases:
        result_two_ptr = sol.threeSumClosest(list(nums), target)
        result_brute = sol.threeSumClosestBruteForce(list(nums), target)
        status = "PASS" if result_two_ptr == expected else "FAIL"
        if result_two_ptr != expected or result_brute != expected:
            all_passed = False
        print(f"[{status}] threeSumClosest({nums}, target={target}) = "
              f"{result_two_ptr} (expected {expected}) | brute force = {result_brute}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()