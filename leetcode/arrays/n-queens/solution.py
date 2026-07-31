"""
51. N-Queens
https://leetcode.com/problems/n-queens/

The n-queens puzzle is the problem of placing n queens on an n x n
chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens
puzzle. You may return the answer in any order. Each solution
contains a distinct board configuration of the n-queens' placement,
where 'Q' and '.' both indicate a queen and an empty space,
respectively.

Example:
    Input:  n = 4
    Output: [[".Q..","...Q","Q...","..Q."],
              ["..Q.","Q...","...Q",".Q.."]]

    Input:  n = 1
    Output: [["Q"]]

Constraints:
    1 <= n <= 9
"""

from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        Approach 1: Row-by-row backtracking with O(1) attack checks
        via three boolean sets.

        Since no two queens can ever share a row (there's exactly one
        queen per row), the search only needs to decide, for each row
        in turn, which column to place a queen in. A placement at
        (row, col) is safe as long as no earlier queen shares its:
          - column                 -> tracked by `cols`
          - "/" diagonal           -> cells with the same (row + col)
                                       -> tracked by `diag1`
          - "\" diagonal           -> cells with the same (row - col)
                                       -> tracked by `diag2`

        Using sets for these three lets every safety check and update
        happen in O(1), instead of re-scanning previously placed
        queens on every attempt.

        Time:  O(n!) -- the branching factor shrinks by roughly one
               per row as columns/diagonals get ruled out, matching
               the classic n-queens search-space bound.
        Space: O(n^2) for the boards produced, O(n) for the
               recursion stack and the three tracking sets.
        """
        result: List[List[str]] = []
        cols: set = set()
        diag1: set = set()  # row + col
        diag2: set = set()  # row - col
        queen_col_per_row: List[int] = [-1] * n

        def backtrack(row: int) -> None:
            if row == n:
                board = []
                for r in range(n):
                    c = queen_col_per_row[r]
                    board.append("." * c + "Q" + "." * (n - c - 1))
                result.append(board)
                return

            for col in range(n):
                if col in cols or (row + col) in diag1 or (row - col) in diag2:
                    continue

                cols.add(col)
                diag1.add(row + col)
                diag2.add(row - col)
                queen_col_per_row[row] = col

                backtrack(row + 1)

                cols.remove(col)
                diag1.remove(row + col)
                diag2.remove(row - col)
                queen_col_per_row[row] = -1

        backtrack(0)
        return result

    def solveNQueensBitmask(self, n: int) -> List[List[str]]:
        """
        Approach 2: Row-by-row backtracking with bitmask attack tracking.

        Same row-by-row idea as approach 1, but instead of three
        Python `set`s, the "columns under attack", "'/' diagonals
        under attack", and "'\' diagonals under attack" are each
        represented as a single integer bitmask, where bit `i` is 1 if
        that column/diagonal is occupied.

        At each row, `available = ((1 << n) - 1) & ~(cols | diag1 | diag2)`
        gives every column that's simultaneously free in all three
        dimensions in one shot; `available & -available` (a classic
        bit trick) extracts the lowest set bit, i.e. the next column
        to try. This trades Python-level set operations for bitwise
        operations, which is typically faster in practice despite the
        same asymptotic complexity.

        Time:  O(n!) -- same search space as approach 1.
        Space: O(n^2) for the boards produced, O(n) for the recursion
               stack and per-row bitmasks.
        """
        result: List[List[str]] = []
        full_mask = (1 << n) - 1
        queen_col_per_row: List[int] = [-1] * n

        def backtrack(row: int, cols: int, diag1: int, diag2: int) -> None:
            if row == n:
                board = []
                for r in range(n):
                    c = queen_col_per_row[r]
                    board.append("." * c + "Q" + "." * (n - c - 1))
                result.append(board)
                return

            available = full_mask & ~(cols | diag1 | diag2)
            while available:
                bit = available & (-available)  # lowest set bit
                col = bit.bit_length() - 1
                queen_col_per_row[row] = col

                backtrack(
                    row + 1,
                    cols | bit,
                    (diag1 | bit) << 1,
                    (diag2 | bit) >> 1,
                )

                available &= available - 1  # clear the lowest set bit
            queen_col_per_row[row] = -1

        backtrack(0, 0, 0, 0)
        return result


def _normalize(solutions: List[List[str]]):
    return sorted(tuple(board) for board in solutions)


def _is_valid_solution(board: List[str], n: int) -> bool:
    positions = []
    for row, line in enumerate(board):
        assert len(line) == n
        col = line.index("Q")
        assert line.count("Q") == 1
        positions.append((row, col))

    for i in range(len(positions)):
        r1, c1 = positions[i]
        for j in range(i + 1, len(positions)):
            r2, c2 = positions[j]
            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


def run_tests() -> None:
    solution = Solution()

    # Known solution counts for n = 1..9 (n = 2, 3 have zero solutions).
    expected_counts = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}

    expected_n4 = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."],
    ]
    expected_n1 = [["Q"]]

    methods = [
        ("solveNQueens (sets)", solution.solveNQueens),
        ("solveNQueensBitmask (bitmask)", solution.solveNQueensBitmask),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for n, expected_count in expected_counts.items():
            actual = method(n)

            assert len(actual) == expected_count, (
                f"FAILED for {name} with n={n}: expected {expected_count} "
                f"solutions, got {len(actual)}"
            )

            for board in actual:
                assert _is_valid_solution(board, n), (
                    f"FAILED for {name} with n={n}: invalid board {board}"
                )

            if n == 4:
                assert _normalize(actual) == _normalize(expected_n4), (
                    f"FAILED for {name} with n=4: exact match mismatch\n"
                    f"  expected={expected_n4}\n  actual={actual}"
                )
            if n == 1:
                assert _normalize(actual) == _normalize(expected_n1), (
                    f"FAILED for {name} with n=1: exact match mismatch"
                )

            print(f"  n={n}: {len(actual)} valid solution(s) -- passed")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()