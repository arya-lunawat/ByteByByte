"""
LeetCode 11 - Container With Most Water
https://leetcode.com/problems/container-with-most-water/

You are given an integer array height of length n. There are n vertical
lines drawn such that the two endpoints of the i-th line are (i, 0) and
(i, height[i]).

Find two lines that together with the x-axis form a container, such that
the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49
    Explanation: The vertical lines are represented by the array
    [1,8,6,2,5,4,8,3,7]. The max area of water the container can contain
    is 49 (between index 1 and index 8: min(8, 7) * (8 - 1) = 7 * 7 = 49).

Example 2:
    Input: height = [1,1]
    Output: 1

Constraints:
    n == height.length
    2 <= n <= 10^5
    0 <= height[i] <= 10^4
"""


class Solution:
    def maxArea(self, height: list[int]) -> int:
        """
        Two-pointer solution.

        Start with the widest possible container (leftmost and rightmost
        lines). The area is limited by the shorter of the two lines, so
        moving the taller pointer inward can only shrink the width without
        any chance of increasing the limiting height - it can never help.
        Moving the shorter pointer inward, however, might find a taller
        line that increases the area despite the reduced width. So we
        always move the pointer at the shorter line inward, tracking the
        best area seen along the way.

        Time Complexity:  O(n) - single pass with two pointers
        Space Complexity: O(1)
        """
        left, right = 0, len(height) - 1
        best = 0

        while left < right:
            h = min(height[left], height[right])
            width = right - left
            best = max(best, h * width)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return best

    def maxAreaBruteForce(self, height: list[int]) -> int:
        """
        Brute-force O(n^2) solution, provided for comparison: check every
        pair of lines.

        Time Complexity:  O(n^2)
        Space Complexity: O(1)
        """
        best = 0
        n = len(height)
        for i in range(n):
            for j in range(i + 1, n):
                h = min(height[i], height[j])
                best = max(best, h * (j - i))
        return best


def run_tests():
    sol = Solution()
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([1, 2, 4, 3], 4),
        ([0, 2], 0),
        ([2, 3, 4, 5, 18, 17, 6], 17),
    ]

    all_passed = True
    for height, expected in test_cases:
        result_two_ptr = sol.maxArea(height)
        result_brute = sol.maxAreaBruteForce(height)
        status = "PASS" if result_two_ptr == expected else "FAIL"
        if result_two_ptr != expected or result_brute != expected:
            all_passed = False
        print(f"[{status}] maxArea({height}) = {result_two_ptr} "
              f"(expected {expected}) | brute force = {result_brute}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()