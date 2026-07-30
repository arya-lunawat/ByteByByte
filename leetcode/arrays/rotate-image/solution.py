"""
48. Rotate Image
https://leetcode.com/problems/rotate-image/

You are given an n x n 2D matrix representing an image. Rotate the
image by 90 degrees (clockwise), in-place: you must modify the input
matrix directly, without allocating another 2D matrix.

Example:
    Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output:          [[7,4,1],[8,5,2],[9,6,3]]

Constraints:
    n == matrix.length == matrix[i].length
    1 <= n <= 20
    -1000 <= matrix[i][j] <= 1000
"""

from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Approach 1: Transpose, then reverse each row.

        A 90-degree clockwise rotation is exactly the composition of
        two simpler in-place operations:
          1. Transpose the matrix (flip across the main diagonal, so
             matrix[i][j] and matrix[j][i] swap).
          2. Reverse every row.

        Why that works: after transposing, row i holds what will
        become column i of the final result, but top-to-bottom
        instead of the needed bottom-to-top order along that column
        -- reversing each row fixes that.

        Time:  O(n^2) -- every cell is touched a constant number of times.
        Space: O(1) extra -- all swaps happen in place on `matrix`.

        Modifies `matrix` in place; returns None per the problem's
        interface.
        """
        n = len(matrix)

        # Step 1: transpose in place (only need the upper triangle,
        # since each swap handles both (i, j) and (j, i)).
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Step 2: reverse each row.
        for row in matrix:
            row.reverse()

    def rotateLayerByLayer(self, matrix: List[List[int]]) -> None:
        """
        Approach 2: Rotate in place, layer by layer, four cells at a time.

        Think of the matrix as concentric square "rings" (layers).
        For each layer, walk along its top edge; for every position,
        cycle the four corresponding cells -- top, right, bottom, left
        -- one step clockwise using a single temp variable:

            temp          <- top
            top           <- left
            left          <- bottom
            bottom        <- right
            right         <- temp

        This is the "manual" version of the same rotation, without
        relying on transpose/reverse as building blocks -- useful for
        understanding *why* the rotation works at the level of
        individual elements.

        Time:  O(n^2) -- every cell is moved exactly once.
        Space: O(1) extra -- one temp variable per 4-cycle.

        Modifies `matrix` in place; returns None per the problem's
        interface.
        """
        n = len(matrix)
        for layer in range(n // 2):
            first, last = layer, n - 1 - layer
            for i in range(first, last):
                offset = i - first

                top = matrix[first][i]

                # left -> top
                matrix[first][i] = matrix[last - offset][first]

                # bottom -> left
                matrix[last - offset][first] = matrix[last][last - offset]

                # right -> bottom
                matrix[last][last - offset] = matrix[i][last]

                # top (saved) -> right
                matrix[i][last] = top


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        ),
        (
            [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
            [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]],
        ),
        ([[1]], [[1]]),
        ([[1, 2], [3, 4]], [[3, 1], [4, 2]]),
        (
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]],
        ),
        ([[-1, -2], [-3, -4]], [[-3, -1], [-4, -2]]),
        (
            [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15],
             [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]],
            [[21, 16, 11, 6, 1], [22, 17, 12, 7, 2], [23, 18, 13, 8, 3],
             [24, 19, 14, 9, 4], [25, 20, 15, 10, 5]],
        ),
        ([[0, 0], [0, 0]], [[0, 0], [0, 0]]),
    ]

    methods = [
        ("rotate (transpose + reverse rows)", solution.rotate),
        ("rotateLayerByLayer (4-cycle per layer)", solution.rotateLayerByLayer),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (matrix, expected) in enumerate(test_cases, 1):
            working = [row[:] for row in matrix]  # deep copy since rotate mutates
            result = method(working)
            assert result is None, (
                f"Test {i} FAILED for {name}: should return None, got {result}"
            )
            assert working == expected, (
                f"Test {i} FAILED for {name}: input={matrix}\n"
                f"  expected={expected}\n  actual={working}"
            )
            print(f"  Test {i} passed: n={len(matrix)}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()