"""
53. Maximum Subarray
https://leetcode.com/problems/maximum-subarray/

Given an integer array nums, find the subarray with the largest sum,
and return its sum. A subarray is a contiguous non-empty sequence of
elements within an array.

Example:
    Input:  nums = [-2,1,-3,4,-1,2,1,-5,4]
    Output: 6
    Explanation: The subarray [4,-1,2,1] has the largest sum 6.

    Input:  nums = [1]
    Output: 1

    Input:  nums = [5,4,-1,7,8]
    Output: 23

Constraints:
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4

Follow up: If you have figured out the O(n) solution, try coding
another solution using the divide and conquer approach, which is
more subtle.
"""

from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Approach 1: Kadane's algorithm.

        Walk the array once, tracking `current_sum`, the best sum of a
        subarray *ending exactly at the current index*. At each step
        there are only two options for that subarray: extend the
        previous best-ending-here subarray by adding the current
        element, or start fresh at the current element (which wins
        exactly when the running sum so far has gone negative, since
        adding a negative prefix can only hurt). The overall answer is
        the max of `current_sum` seen across all positions.

        current_sum = max(nums[i], current_sum + nums[i])

        Time:  O(n) -- single pass over the array.
        Space: O(1) -- two running variables, no extra storage.
        """
        current_sum = best_sum = nums[0]
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            best_sum = max(best_sum, current_sum)
        return best_sum

    def maxSubArrayDivideConquer(self, nums: List[int]) -> int:
        """
        Approach 2: Divide and conquer.

        Split the array in half at each step. The maximum subarray
        sum for a range is the best of three candidates:
          1. The best subarray entirely within the left half.
          2. The best subarray entirely within the right half.
          3. The best subarray that *crosses* the midpoint, found by
             extending as far left as possible (max prefix sum ending
             at mid) and as far right as possible (max suffix sum
             starting at mid+1), then adding those two together.

        Base case: a single element's best subarray is itself.

        Time:  O(n log n) -- log n levels of recursion, each doing
               O(n) work to find the best crossing subarray.
        Space: O(log n) recursion stack depth.

        This is the "more subtle" solution mentioned in the problem's
        follow-up -- asymptotically worse than Kadane's O(n), but a
        good exercise in the divide-and-conquer pattern (and it's the
        same structural idea used in problems like the closest-pair or
        max-crossing-sum variants).
        """

        def max_crossing_sum(arr: List[int], low: int, mid: int, high: int) -> int:
            left_sum = float("-inf")
            running = 0
            for i in range(mid, low - 1, -1):
                running += arr[i]
                left_sum = max(left_sum, running)

            right_sum = float("-inf")
            running = 0
            for i in range(mid + 1, high + 1):
                running += arr[i]
                right_sum = max(right_sum, running)

            return left_sum + right_sum

        def helper(arr: List[int], low: int, high: int) -> int:
            if low == high:
                return arr[low]

            mid = (low + high) // 2
            left_best = helper(arr, low, mid)
            right_best = helper(arr, mid + 1, high)
            cross_best = max_crossing_sum(arr, low, mid, high)

            return max(left_best, right_best, cross_best)

        return helper(nums, 0, len(nums) - 1)


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-1], -1),
        ([-3, -2, -1], -1),
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3, -4], -1),
        ([0, 0, 0], 0),
        ([8, -19, 5, -4, 20], 21),
        (list(range(-5, 6)), 15),  # [-5,-4,...,5] -> best subarray [1..5] or full suffix
    ]

    methods = [
        ("maxSubArray (Kadane's)", solution.maxSubArray),
        ("maxSubArrayDivideConquer (divide and conquer)", solution.maxSubArrayDivideConquer),
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