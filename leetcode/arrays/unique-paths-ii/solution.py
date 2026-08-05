"""
63. Unique Paths II
https://leetcode.com/problems/unique-paths-ii/

You are given an m x n integer array grid. There is a robot initially
located at the top-left corner (grid[0][0]). The robot tries to move
to the bottom-right corner (grid[m-1][n-1]). The robot can only move
either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A
path that the robot takes cannot include any square that is an
obstacle.

Return the number of possible unique paths that the robot can take to
reach the bottom-right corner.

Example:
    Input:  obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
    Output: 2
    Explanation: There is one obstacle in the middle of the 3x3 grid.
    There are two ways to reach the bottom-right corner:
    1. Right -> Right -> Down -> Down
    2. Down -> Down -> Right -> Right

    Input:  obstacleGrid = [[0,1],[0,0]]
    Output: 1

Constraints:
    m == obstacleGrid.length
    n == obstacleGrid[i].length
    1 <= m, n <= 100
    obstacleGrid[i][j] is 0 or 1.
"""

from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        """
        Approach 1: Dynamic programming with a rolling 1D row.

        Same recurrence idea as the obstacle-free version (problem 62)
        -- dp[j] = ways to reach the cell above + ways to reach the
        cell to the left -- with one addition: any obstacle cell has
        exactly zero ways to be reached, since the robot can never
        stand on it. So whenever the current cell is an obstacle,
        dp[j] is forced to 0 regardless of what it would otherwise sum
        to; this single override handles obstacles anywhere in the
        grid, including the very first cell (making the answer 0
        immediately) or an obstacle blocking off an entire row/column.

        Time:  O(m * n) -- one check + possible addition per cell.
        Space: O(n) -- a single rolling row, instead of a full
               O(m * n) 2D table.
        """
        if not obstacleGrid or not obstacleGrid[0]:
            return 0

        rows, cols = len(obstacleGrid), len(obstacleGrid[0])
        if obstacleGrid[0][0] == 1:
            return 0

        dp = [0] * cols
        dp[0] = 1

        for i in range(rows):
            for j in range(cols):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0
                elif j > 0:
                    dp[j] += dp[j - 1]
                # j == 0 and not an obstacle: dp[0] carries over
                # unchanged from the row above (moving straight down
                # the first column), so no update needed here.

        return dp[-1]

    def uniquePathsWithObstacles2D(self, obstacleGrid: List[List[int]]) -> int:
        """
        Approach 2: Dynamic programming with a full 2D table.

        The more explicit version of the same idea: build a full
        (rows x cols) table where dp[i][j] holds the number of ways to
        reach cell (i, j). An obstacle cell is always 0. Otherwise,
        dp[i][j] = dp[i-1][j] + dp[i][j-1] (falling back to 0 for any
        out-of-bounds neighbor, i.e. the top row/left column only ever
        get contributions from one direction). The starting cell
        dp[0][0] is seeded as 1 unless it's itself an obstacle.

        This uses more memory than the rolling-row version but keeps
        every intermediate state visible, which can make it easier to
        debug or to adapt for problems that need to look back further
        than one row.

        Time:  O(m * n) -- one computation per cell.
        Space: O(m * n) -- the full 2D table.
        """
        if not obstacleGrid or not obstacleGrid[0]:
            return 0

        rows, cols = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                elif i == 0 and j == 0:
                    dp[i][j] = 1
                else:
                    from_top = dp[i - 1][j] if i > 0 else 0
                    from_left = dp[i][j - 1] if j > 0 else 0
                    dp[i][j] = from_top + from_left

        return dp[-1][-1]


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2),
        ([[0, 1], [0, 0]], 1),
        ([[0]], 1),
        ([[1]], 0),
        ([[0, 0]], 1),
        ([[0], [0]], 1),
        ([[1, 0]], 0),
        ([[0, 0], [1, 1], [0, 0]], 0),
        ([[0, 0, 0]], 1),
        (
            [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            3,
        ),
    ]

    methods = [
        ("uniquePathsWithObstacles (DP, rolling row)", solution.uniquePathsWithObstacles),
        ("uniquePathsWithObstacles2D (DP, full table)", solution.uniquePathsWithObstacles2D),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (grid, expected) in enumerate(test_cases, 1):
            grid_copy = [row[:] for row in grid]
            actual = method(grid_copy)
            assert actual == expected, (
                f"Test {i} FAILED for {name}: grid={grid}\n"
                f"  expected={expected}, actual={actual}"
            )
            print(f"  Test {i} passed: grid={grid} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()