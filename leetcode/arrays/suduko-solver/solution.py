"""
LeetCode 37 - Sudoku Solver
https://leetcode.com/problems/sudoku-solver/

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:
1. Each of the digits 1-9 must occur exactly once in each row.
2. Each of the digits 1-9 must occur exactly once in each column.
3. Each of the digits 1-9 must occur exactly once in each of the nine
   3 x 3 sub-boxes of the grid.

The '.' character indicates empty cells. The board is modified in
place, and the puzzle is guaranteed to have exactly one solution.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Plain backtracking, re-validating from scratch every time.

    Scan for the next empty cell, try digits '1'-'9' in order, and for
    each candidate re-check the entire row, column, and 3x3 box by
    scanning them directly (no cached state). If a digit is valid,
    place it and recurse; if the recursive call fails, undo ('.') and
    try the next digit. If no digit works, backtrack.

    This is correct but slow in practice: every single placement
    attempt re-scans up to 27 cells (9 row + 9 col + 9 box) just to
    check validity, on top of the exponential backtracking search
    itself.

    Time:  Exponential in the worst case (backtracking search), with a
           significant constant-factor overhead per attempted
           placement from the repeated O(1)-ish-but-not-cached
           row/col/box scans (technically O(9) per scan x 3 scans).
    Space: O(1) extra (aside from recursion stack), since validity is
           checked directly against the board each time.
    """

    def solveSudoku(self, board: List[List[str]]) -> None:
        self._solve(board)

    def _solve(self, board: List[List[str]]) -> bool:
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for digit in "123456789":
                        if self._is_valid(board, r, c, digit):
                            board[r][c] = digit
                            if self._solve(board):
                                return True
                            board[r][c] = "."
                    return False  # no digit worked here -> backtrack
        return True  # no empty cells left -> solved

    def _is_valid(self, board: List[List[str]], row: int, col: int, digit: str) -> bool:
        for i in range(9):
            if board[row][i] == digit:
                return False
            if board[i][col] == digit:
                return False
            box_r = 3 * (row // 3) + i // 3
            box_c = 3 * (col // 3) + i % 3
            if board[box_r][box_c] == digit:
                return False
        return True


class Solution:
    """
    Approach: Backtracking with cached constraint sets + MRV heuristic.

    Two optimizations over the brute-force version:

    1. **O(1) validity checks.** Maintain 9 row sets, 9 column sets,
       and 9 box sets (same box-indexing scheme as Valid Sudoku:
       `(r // 3) * 3 + (c // 3)`), each holding the digits already
       used in that row/column/box. Placing or removing a digit is an
       O(1) set add/discard, and checking whether a digit is safe to
       place is an O(1) set membership test -- no re-scanning 27 cells
       per attempt.

    2. **Most-constrained-cell-first (MRV heuristic).** Instead of
       always filling empty cells in reading order, at each step pick
       the empty cell with the *fewest* remaining valid candidate
       digits. Cells that are almost fully constrained (e.g. only 1
       possible digit) get resolved first, which fails fast on dead
       branches and dramatically prunes the search tree compared to a
       fixed left-to-right, top-to-bottom fill order.

    Time:  Exponential in the worst case (Sudoku solving is NP-complete
           in general grid sizes), but the constant-factor savings from
           O(1) constraint checks and the MRV heuristic's aggressive
           pruning make this dramatically faster in practice than the
           brute-force version on real puzzles.
    Space: O(1) extra for the 27 constraint sets (bounded by the fixed
           9x9 board size), plus O(81) recursion depth in the worst
           case.
    """

    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empties = []

        for r in range(9):
            for c in range(9):
                digit = board[r][c]
                if digit == ".":
                    empties.append((r, c))
                else:
                    rows[r].add(digit)
                    cols[c].add(digit)
                    boxes[(r // 3) * 3 + (c // 3)].add(digit)

        def candidates(r: int, c: int):
            box_idx = (r // 3) * 3 + (c // 3)
            used = rows[r] | cols[c] | boxes[box_idx]
            return [d for d in "123456789" if d not in used]

        def backtrack() -> bool:
            if not empties:
                return True

            # MRV: pick the empty cell with the fewest valid candidates.
            best_idx, best_cell, best_candidates = -1, None, None
            for idx, (r, c) in enumerate(empties):
                cand = candidates(r, c)
                if best_candidates is None or len(cand) < len(best_candidates):
                    best_idx, best_cell, best_candidates = idx, (r, c), cand
                    if len(cand) <= 1:
                        break  # can't do better than 0 or 1 candidates

            if not best_candidates:
                return False  # dead end: an empty cell has no valid digit

            r, c = best_cell
            box_idx = (r // 3) * 3 + (c // 3)
            empties.pop(best_idx)

            for digit in best_candidates:
                board[r][c] = digit
                rows[r].add(digit)
                cols[c].add(digit)
                boxes[box_idx].add(digit)

                if backtrack():
                    return True

                board[r][c] = "."
                rows[r].discard(digit)
                cols[c].discard(digit)
                boxes[box_idx].discard(digit)

            empties.insert(best_idx, (r, c))
            return False

        backtrack()


def board_to_str(board: List[List[str]]) -> str:
    return "\n".join(" ".join(row) for row in board)


if __name__ == "__main__":
    puzzle = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]

    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]

    board_brute = [row[:] for row in puzzle]
    SolutionBruteForce().solveSudoku(board_brute)
    status_brute = "PASS" if board_brute == expected else "FAIL"

    board_opt = [row[:] for row in puzzle]
    Solution().solveSudoku(board_opt)
    status_opt = "PASS" if board_opt == expected else "FAIL"

    print(f"Brute force solve: [{status_brute}]")
    print(f"Optimal (MRV) solve: [{status_opt}]")
    print()
    print("Solved board (optimal):")
    print(board_to_str(board_opt))