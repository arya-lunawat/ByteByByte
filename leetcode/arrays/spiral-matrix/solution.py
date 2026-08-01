"""
54. Spiral Matrix
https://leetcode.com/problems/spiral-matrix/

Given an m x n matrix, return all elements of the matrix in spiral
order.

Example:
    Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [1,2,3,6,9,8,7,4,5]

    Input:  matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    Output: [1,2,3,4,8,12,11,10,9,5,6,7]

Constraints:
    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 10
    -100 <= matrix[i][j] <= 100
"""

from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Approach 1: Shrinking boundaries (top/bottom/left/right).

        Track four boundaries -- top, bottom, left, right -- that
        define the still-unvisited rectangle. Repeatedly walk:
          - left -> right along the `top` row, then push `top` down,
          - top -> bottom along the `right` column, then pull `right` in,
          - right -> left along the `bottom` row (if a row remains),
            then pull `bottom` up,
          - bottom -> top along the `left` column (if a column remains),
            then push `left` in,
        and repeat until the boundaries cross. The two "if a row/column
        remains" guards are what prevent re-visiting cells on the final
        single row or single column of a non-square matrix.

        Time:  O(m * n) -- every cell is visited exactly once.
        Space: O(1) extra, not counting the output list.
        """
        if not matrix or not matrix[0]:
            return []

        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result

    def spiralOrderSimulation(self, matrix: List[List[int]]) -> List[int]:
        """
        Approach 2: Direct simulation with a "turn on wall or visited"
        rule.

        Walk the matrix one cell at a time in a current direction
        (right, down, left, up, cycling in that order). Mark each
        visited cell so it's never re-added, and whenever the next
        step would leave the grid or land on an already-visited cell,
        turn 90 degrees clockwise instead. Stop once every cell has
        been visited.

        This is a more literal "trace the path" simulation, which can
        be easier to adapt to variations of the problem (e.g., spiral
        fill instead of spiral read) than the boundary-shrinking
        version, at the cost of needing an explicit visited matrix.

        Time:  O(m * n) -- every cell is visited exactly once.
        Space: O(m * n) for the `visited` matrix.
        """
        if not matrix or not matrix[0]:
            return []

        rows, cols = len(matrix), len(matrix[0])
        visited = [[False] * cols for _ in range(rows)]
        result = []

        # Directions cycle: right, down, left, up.
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dir_index = 0
        row, col = 0, 0

        for _ in range(rows * cols):
            result.append(matrix[row][col])
            visited[row][col] = True

            dr, dc = directions[dir_index]
            next_row, next_col = row + dr, col + dc

            if (
                not (0 <= next_row < rows and 0 <= next_col < cols)
                or visited[next_row][next_col]
            ):
                dir_index = (dir_index + 1) % 4
                dr, dc = directions[dir_index]
                next_row, next_col = row + dr, col + dc

            row, col = next_row, next_col

        return result


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
        (
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
        ),
        ([[1]], [1]),
        ([[1, 2, 3]], [1, 2, 3]),
        ([[1], [2], [3]], [1, 2, 3]),
        ([[1, 2], [3, 4]], [1, 2, 4, 3]),
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
            [1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8],
        ),
        ([[-1, -2], [-3, -4], [-5, -6]], [-1, -2, -4, -6, -5, -3]),
    ]

    methods = [
        ("spiralOrder (shrinking boundaries)", solution.spiralOrder),
        ("spiralOrderSimulation (walk + turn)", solution.spiralOrderSimulation),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (matrix, expected) in enumerate(test_cases, 1):
            actual = method(matrix)
            assert actual == expected, (
                f"Test {i} FAILED for {name}: matrix={matrix}\n"
                f"  expected={expected}\n  actual={actual}"
            )
            print(f"  Test {i} passed: {len(matrix)}x{len(matrix[0])} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()