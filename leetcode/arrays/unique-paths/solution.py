"""
62. Unique Paths
https://leetcode.com/problems/unique-paths/

There is a robot on an m x n grid. The robot is initially located at
the top-left corner. The robot tries to move to the bottom-right
corner. The robot can only move either down or right at any point in
time.

Given the two integers m and n, return the number of possible unique
paths that the robot can take to reach the bottom-right corner.

Example:
    Input:  m = 3, n = 7
    Output: 28

    Input:  m = 3, n = 2
    Output: 3
    Explanation: From the top-left corner, there are a total of 3
    ways to reach the bottom-right corner:
    1. Right -> Down -> Down
    2. Down -> Down -> Right
    3. Down -> Right -> Down

Constraints:
    1 <= m, n <= 100
"""

from math import comb


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Approach 1: Dynamic programming with a rolling 1D row.

        Let dp[j] represent the number of unique paths to reach column
        j of the *current* row. The number of ways to reach any cell
        is the sum of the ways to reach the cell above it (moving
        down) and the cell to its left (moving right):

            dp[j] = dp[j] (from the row above, not yet overwritten)
                    + dp[j - 1] (from the same row, already updated)

        Initialize the first row to all 1s (only one way to reach any
        cell in the top row -- move right repeatedly), then update the
        same array in place for each subsequent row, left to right,
        since dp[j-1] needs to already reflect the current row while
        dp[j] still holds the previous row's value at the moment it's
        read.

        Time:  O(m * n) -- one addition per cell.
        Space: O(n) -- a single rolling row, instead of the full
               O(m * n) 2D table.
        """
        dp = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[-1]

    def uniquePathsCombinatorics(self, m: int, n: int) -> int:
        """
        Approach 2: Direct combinatorics.

        Every path from the top-left to the bottom-right corner
        consists of exactly (m - 1) "down" moves and (n - 1) "right"
        moves, in some order -- a total of (m - 1) + (n - 1) moves.
        The number of distinct paths is exactly the number of ways to
        choose which of those move-slots are "down" moves (the rest
        being "right" moves), which is the binomial coefficient:

            C(m + n - 2, m - 1)

        Python's math.comb computes this directly and exactly (no
        floating-point rounding), making this the fastest approach by
        far -- a single combinatorial computation instead of filling
        an O(m * n) table.

        Time:  O(min(m, n)) -- math.comb's internal computation is
               roughly linear in the smaller of the two chosen values.
        Space: O(1) -- no table at all.
        """
        return comb(m + n - 2, m - 1)


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        (3, 7, 28),
        (3, 2, 3),
        (1, 1, 1),
        (1, 10, 1),
        (10, 1, 1),
        (7, 3, 28),
        (2, 2, 2),
        (23, 12, 193536720),
        (100, 100, 22750883079422934966181954039568885395604168260154104734000),
        (5, 5, 70),
    ]

    methods = [
        ("uniquePaths (DP, rolling row)", solution.uniquePaths),
        ("uniquePathsCombinatorics (math.comb)", solution.uniquePathsCombinatorics),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (m, n, expected) in enumerate(test_cases, 1):
            actual = method(m, n)
            assert actual == expected, (
                f"Test {i} FAILED for {name}: m={m}, n={n}\n"
                f"  expected={expected}, actual={actual}"
            )
            print(f"  Test {i} passed: m={m}, n={n} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()