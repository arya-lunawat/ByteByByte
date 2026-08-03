"""
59. Spiral Matrix II
https://leetcode.com/problems/spiral-matrix-ii/

Given a positive integer n, generate an n x n matrix filled with
elements from 1 to n^2 in spiral order.

Example:
    Input:  n = 3
    Output: [[1,2,3],[8,9,4],[7,6,5]]

    Input:  n = 1
    Output: [[1]]

Constraints:
    1 <= n <= 20
"""

from typing import List


class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        """
        Approach 1: Shrinking boundaries (top/bottom/left/right), same
        structure as reading a matrix in spiral order (problem 54),
        but writing values 1..n^2 instead of reading them.

        Track four boundaries -- top, bottom, left, right -- that
        define the still-unfilled square. Repeatedly:
          - fill left -> right along the `top` row, then push top down,
          - fill top -> bottom along the `right` column, then pull right in,
          - fill right -> left along the `bottom` row (if a row remains),
            then pull bottom up,
          - fill bottom -> top along the `left` column (if a column
            remains), then push left in,
        incrementing a counter after every cell written, until the
        boundaries cross. Since n x n is always square, the "if a
        row/column remains" guards only ever matter on the very last
        (single-cell) layer, but they're kept for consistency with the
        general spiral-fill pattern.

        Time:  O(n^2) -- every cell is written exactly once.
        Space: O(1) extra, not counting the output matrix itself.
        """
        matrix = [[0] * n for _ in range(n)]
        top, bottom = 0, n - 1
        left, right = 0, n - 1
        value = 1

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                matrix[top][col] = value
                value += 1
            top += 1

            for row in range(top, bottom + 1):
                matrix[row][right] = value
                value += 1
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    matrix[bottom][col] = value
                    value += 1
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    matrix[row][left] = value
                    value += 1
                left += 1

        return matrix

    def generateMatrixSimulation(self, n: int) -> List[List[int]]:
        """
        Approach 2: Direct simulation with a "turn on wall or filled
        cell" rule, mirroring the simulation approach to problem 54.

        Walk the grid one cell at a time in a current direction
        (right, down, left, up, cycling in that order), writing the
        next value into each cell as it's visited. Whenever the next
        step would leave the grid or land on an already-filled cell,
        turn 90 degrees clockwise instead of stepping. Stop once every
        cell has been filled.

        This is a more literal "trace the spiral path" simulation --
        useful for building intuition, or adapting to variants (e.g.
        starting the spiral from a different corner or direction), at
        the cost of needing to check "is this cell already filled"
        instead of using implicit boundary arithmetic.

        Time:  O(n^2) -- every cell is visited exactly once.
        Space: O(1) extra beyond the output matrix (reusing the
               matrix's own 0 vs. non-zero values as the "visited"
               check, rather than a separate visited grid).
        """
        matrix = [[0] * n for _ in range(n)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        dir_index = 0
        row, col = 0, 0

        for value in range(1, n * n + 1):
            matrix[row][col] = value

            dr, dc = directions[dir_index]
            next_row, next_col = row + dr, col + dc

            if (
                not (0 <= next_row < n and 0 <= next_col < n)
                or matrix[next_row][next_col] != 0
            ):
                dir_index = (dir_index + 1) % 4
                dr, dc = directions[dir_index]
                next_row, next_col = row + dr, col + dc

            row, col = next_row, next_col

        return matrix


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        (3, [[1, 2, 3], [8, 9, 4], [7, 6, 5]]),
        (1, [[1]]),
        (2, [[1, 2], [4, 3]]),
        (
            4,
            [
                [1, 2, 3, 4],
                [12, 13, 14, 5],
                [11, 16, 15, 6],
                [10, 9, 8, 7],
            ],
        ),
        (
            5,
            [
                [1, 2, 3, 4, 5],
                [16, 17, 18, 19, 6],
                [15, 24, 25, 20, 7],
                [14, 23, 22, 21, 8],
                [13, 12, 11, 10, 9],
            ],
        ),
    ]

    def is_valid_spiral_content(matrix: List[List[int]], n: int) -> bool:
        flat = sorted(v for row in matrix for v in row)
        return flat == list(range(1, n * n + 1))

    methods = [
        ("generateMatrix (shrinking boundaries)", solution.generateMatrix),
        ("generateMatrixSimulation (walk + turn)", solution.generateMatrixSimulation),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (n, expected) in enumerate(test_cases, 1):
            actual = method(n)
            assert is_valid_spiral_content(actual, n), (
                f"Test {i} FAILED for {name}: n={n} -- doesn't contain "
                f"exactly 1..n^2, got {actual}"
            )
            assert actual == expected, (
                f"Test {i} FAILED for {name}: n={n}\n"
                f"  expected={expected}\n  actual={actual}"
            )
            print(f"  Test {i} passed: n={n} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()