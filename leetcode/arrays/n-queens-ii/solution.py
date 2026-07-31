"""
52. N-Queens II
https://leetcode.com/problems/n-queens-ii/

The n-queens puzzle is the problem of placing n queens on an n x n
chessboard such that no two queens attack each other.

Given an integer n, return the number of distinct solutions to the
n-queens puzzle.

Example:
    Input:  n = 4
    Output: 2
    Explanation: There are two distinct solutions to the 4-queens
    puzzle as shown.

    Input:  n = 1
    Output: 1

Constraints:
    1 <= n <= 9
"""


class Solution:
    def totalNQueens(self, n: int) -> int:
        """
        Approach 1: Row-by-row backtracking with three tracking sets,
        counting only (no boards built).

        This is the counting-only twin of problem 51 (N-Queens): since
        no two queens can share a row, the search just decides, one
        row at a time, which column gets the queen for that row. A
        placement at (row, col) is safe as long as no earlier queen
        shares its:
          - column                 -> tracked by `cols`
          - "/" diagonal           -> cells with equal (row + col)
                                       -> tracked by `diag1`
          - "\" diagonal           -> cells with equal (row - col)
                                       -> tracked by `diag2`

        Since problem 52 only asks for a *count*, there's no need to
        materialize board strings at all -- just increment a counter
        every time a full valid placement (row == n) is reached. This
        saves the O(n^2) per-solution board-building cost that N-Queens
        (51) requires.

        Time:  O(n!) -- same n-queens search-space bound as problem 51.
        Space: O(n) for the recursion stack and the three tracking sets
               (no O(n^2) boards to store).
        """
        count = 0
        cols: set = set()
        diag1: set = set()  # row + col
        diag2: set = set()  # row - col

        def backtrack(row: int) -> None:
            nonlocal count
            if row == n:
                count += 1
                return

            for col in range(n):
                if col in cols or (row + col) in diag1 or (row - col) in diag2:
                    continue

                cols.add(col)
                diag1.add(row + col)
                diag2.add(row - col)

                backtrack(row + 1)

                cols.remove(col)
                diag1.remove(row + col)
                diag2.remove(row - col)

        backtrack(0)
        return count

    def totalNQueensBitmask(self, n: int) -> int:
        """
        Approach 2: Row-by-row backtracking with bitmask attack
        tracking, counting only.

        Same row-by-row search as approach 1, but "columns attacked",
        "'/' diagonals attacked", and "'\' diagonals attacked" are each
        packed into a single integer bitmask instead of a Python set.
        At each row:

            available = full_mask & ~(cols | diag1 | diag2)

        gives every column that's simultaneously free in all three
        dimensions in one shot, and the classic bit trick
        `available & -available` pulls out the lowest set bit -- the
        next column to try -- without looping over every column index
        individually. Bitwise operations are typically faster in
        practice than the equivalent set operations.

        Time:  O(n!) -- same search space as approach 1.
        Space: O(n) for the recursion stack and per-call bitmasks.
        """
        full_mask = (1 << n) - 1

        def backtrack(row: int, cols: int, diag1: int, diag2: int) -> int:
            if row == n:
                return 1

            count = 0
            available = full_mask & ~(cols | diag1 | diag2)
            while available:
                bit = available & (-available)  # lowest set bit
                count += backtrack(
                    row + 1,
                    cols | bit,
                    (diag1 | bit) << 1,
                    (diag2 | bit) >> 1,
                )
                available &= available - 1  # clear the lowest set bit
            return count

        return backtrack(0, 0, 0, 0)


def run_tests() -> None:
    solution = Solution()

    # Known solution counts for n = 1..9 (n = 2, 3 have zero solutions).
    expected_counts = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}

    methods = [
        ("totalNQueens (sets)", solution.totalNQueens),
        ("totalNQueensBitmask (bitmask)", solution.totalNQueensBitmask),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for n, expected in expected_counts.items():
            actual = method(n)
            assert actual == expected, (
                f"FAILED for {name} with n={n}: expected {expected}, got {actual}"
            )
            print(f"  n={n}: {actual} solution(s) -- passed")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()