"""
64. Minimum Path Sum
https://leetcode.com/problems/minimum-path-sum/

Given an m x n grid filled with non-negative numbers, find a path
from top left to bottom right, which minimizes the sum of all numbers
along its path. You can only move either down or right at any point
in time.

Example:
    Input:  grid = [[1,3,1],[1,5,1],[4,2,1]]
    Output: 7
    Explanation: Because the path 1 -> 3 -> 1 -> 1 -> 1 minimizes the sum.

    Input:  grid = [[1,2,3],[4,5,6]]
    Output: 12

Constraints:
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 200
    0 <= grid[i][j] <= 200
"""

from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        """
        Approach 1: In-place dynamic programming on the input grid.

        For any cell (i, j), the cheapest path to it is its own value
        plus whichever of "cheapest path to the cell above" or
        "cheapest path to the cell to the left" is smaller (the two
        directions the robot could have arrived from):

            grid[i][j] += min(grid[i-1][j], grid[i][j-1])

        The first row can only be reached by moving right repeatedly
        (so each cell just accumulates the running sum from its
        left neighbor), and the first column can only be reached by
        moving down repeatedly (accumulating from its top neighbor).
        Updating the grid in place, row by row and left to right,
        means grid[i-1][j] and grid[i][j-1] are always already-finalized
        values by the time cell (i, j) is processed.

        Time:  O(m * n) -- one comparison + addition per cell.
        Space: O(1) extra -- reuses the input grid itself instead of
               allocating a separate DP table.

        Mutates the input grid.
        """
        rows, cols = len(grid), len(grid[0])

        for i in range(rows):
            for j in range(cols):
                if i == 0 and j == 0:
                    continue
                elif i == 0:
                    grid[i][j] += grid[i][j - 1]
                elif j == 0:
                    grid[i][j] += grid[i - 1][j]
                else:
                    grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])

        return grid[-1][-1]

    def minPathSumRollingRow(self, grid: List[List[int]]) -> int:
        """
        Approach 2: Dynamic programming with a rolling 1D row (input
        left untouched).

        Same recurrence as approach 1, but instead of mutating the
        caller's grid, a single reusable row `dp` is maintained. For
        each row of the grid:
          - dp[0] accumulates straight down the first column,
          - every other dp[j] becomes
            grid[i][j] + min(dp[j], dp[j - 1]), where dp[j] (not yet
            overwritten this row) still holds the value from the row
            above, and dp[j - 1] has already been updated for the
            current row.

        Useful when the input grid must not be modified (e.g. it's
        reused elsewhere by the caller), at the cost of allocating one
        extra array of length n.

        Time:  O(m * n) -- one comparison + addition per cell.
        Space: O(n) -- a single rolling row.
        """
        rows, cols = len(grid), len(grid[0])
        dp = [0] * cols
        dp[0] = grid[0][0]
        for j in range(1, cols):
            dp[j] = dp[j - 1] + grid[0][j]

        for i in range(1, rows):
            dp[0] += grid[i][0]
            for j in range(1, cols):
                dp[j] = grid[i][j] + min(dp[j], dp[j - 1])

        return dp[-1]


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
        ([[1, 2, 3], [4, 5, 6]], 12),
        ([[1]], 1),
        ([[0]], 0),
        ([[1, 2, 3]], 6),
        ([[1], [2], [3]], 6),
        ([[0, 0], [0, 0]], 0),
        ([[5, 4], [1, 1]], 7),
        (
            [[1, 3, 1, 2], [1, 5, 1, 1], [4, 2, 1, 3], [1, 1, 2, 1]],
            10,
        ),
        ([[9, 1, 4, 8], [1, 1, 1, 1], [3, 2, 1, 9]], 22),
    ]

    methods = [
        ("minPathSum (in-place DP)", solution.minPathSum),
        ("minPathSumRollingRow (rolling row DP)", solution.minPathSumRollingRow),
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