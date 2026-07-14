"""
LeetCode 22 - Generate Parentheses
https://leetcode.com/problems/generate-parentheses/

Given n pairs of parentheses, write a function to generate all
combinations of well-formed parentheses.

Example 1:
    Input: n = 3
    Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
    Input: n = 1
    Output: ["()"]

Constraints:
    1 <= n <= 8
"""


class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        """
        Backtracking, constrained by counts of remaining open/close
        parens.

        Build the string one character at a time, tracking how many
        opening and closing parentheses have been used so far. At each
        step there are up to two choices:
          - Add '(' if we haven't used all n opening parens yet.
          - Add ')' if doing so wouldn't create more closing than opening
            parens so far (i.e. close_count < open_count).
        A combination is complete once its length reaches 2n. Because we
        only ever make moves that keep the string a valid prefix of some
        well-formed sequence, every completed string is automatically
        valid - no separate validation pass is needed.

        Time Complexity:  O(4^n / sqrt(n)) - the number of valid
                           combinations is the nth Catalan number, and
                           each one takes O(n) to build, giving the
                           well-known Catalan-number bound
        Space Complexity: O(n) for the recursion depth and current path
                           (not counting the output)
        """
        result = []
        path = []

        def backtrack(open_count: int, close_count: int) -> None:
            if len(path) == 2 * n:
                result.append("".join(path))
                return

            if open_count < n:
                path.append("(")
                backtrack(open_count + 1, close_count)
                path.pop()

            if close_count < open_count:
                path.append(")")
                backtrack(open_count, close_count + 1)
                path.pop()

        backtrack(0, 0)
        return result

    def generateParenthesisDP(self, n: int) -> list[str]:
        """
        Alternative solution: dynamic programming built from smaller
        valid combinations.

        Every valid combination of length 2n can be decomposed as
        "(" + (a valid combination of length 2i) + ")" + (a valid
        combination of length 2(n-1-i)), for some split point i from 0 to
        n-1. This mirrors how balanced parentheses naturally split around
        their first matching closing bracket. dp[k] holds all valid
        combinations using k pairs; dp[0] = [""] is the base case.

        Time Complexity:  O(4^n / sqrt(n)) - same Catalan-number bound,
                           just computed bottom-up instead of via direct
                           recursion
        Space Complexity: O(4^n / sqrt(n)) - stores all combinations for
                           every count from 0 to n along the way
        """
        dp = [[] for _ in range(n + 1)]
        dp[0] = [""]

        for k in range(1, n + 1):
            combinations = []
            for i in range(k):
                for left in dp[i]:
                    for right in dp[k - 1 - i]:
                        combinations.append("(" + left + ")" + right)
            dp[k] = combinations

        return dp[n]


def run_tests():
    sol = Solution()
    test_cases = [
        (1, ["()"]),
        (2, ["(())", "()()"]),
        (3, ["((()))", "(()())", "(())()", "()(())", "()()()"]),
    ]

    all_passed = True
    for n, expected in test_cases:
        result_backtrack = sorted(sol.generateParenthesis(n))
        result_dp = sorted(sol.generateParenthesisDP(n))
        expected_sorted = sorted(expected)
        status = "PASS" if result_backtrack == expected_sorted else "FAIL"
        if result_backtrack != expected_sorted or result_dp != expected_sorted:
            all_passed = False
        print(f"[{status}] generateParenthesis({n}) has "
              f"{len(result_backtrack)} combos (expected {len(expected_sorted)}) "
              f"| backtrack == dp: {result_backtrack == result_dp}")

    # Sanity check against the Catalan number formula for a larger n.
    from math import comb
    for n in range(1, 9):
        catalan = comb(2 * n, n) // (n + 1)
        actual = len(sol.generateParenthesis(n))
        status = "PASS" if actual == catalan else "FAIL"
        if actual != catalan:
            all_passed = False
        print(f"[{status}] count for n={n}: {actual} (expected Catalan number {catalan})")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()