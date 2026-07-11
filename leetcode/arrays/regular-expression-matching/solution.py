"""
LeetCode 10 - Regular Expression Matching
https://leetcode.com/problems/regular-expression-matching/

Given an input string s and a pattern p, implement regular expression
matching with support for '.' and '*' where:
    '.' Matches any single character.
    '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Example 1:
    Input: s = "aa", p = "a"
    Output: False
    Explanation: "a" does not match the entire string "aa".

Example 2:
    Input: s = "aa", p = "a*"
    Output: True
    Explanation: '*' means zero or more of the preceding element, 'a'.
    Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
    Input: s = "ab", p = ".*"
    Output: True
    Explanation: ".*" means "zero or more (*) of any character (.)".

Constraints:
    1 <= s.length <= 20
    1 <= p.length <= 30
    s contains only lowercase English letters.
    p contains only lowercase English letters, '.', and '*'.
    It is guaranteed for each appearance of the character '*',
    there will be a previous valid character to match.
"""

from functools import lru_cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Bottom-up dynamic programming solution.

        dp[i][j] = True if s[i:] matches p[j:] (i.e. the suffixes match).

        We build the table from the end of both strings backwards, since
        that's the natural direction '*' expands in (it looks at what
        comes *after* it in the pattern).

        Time Complexity:  O(len(s) * len(p))
        Space Complexity: O(len(s) * len(p))
        """
        m, n = len(s), len(p)

        # dp[i][j] describes whether s[i:] matches p[j:]
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True  # empty string matches empty pattern

        for i in range(m, -1, -1):
            for j in range(n - 1, -1, -1):
                first_match = i < m and p[j] in (s[i], '.')

                if j + 1 < n and p[j + 1] == '*':
                    # Either skip "char*" entirely (zero occurrences),
                    # or, if the first character matches, consume one
                    # character from s and stay on the same pattern
                    # position (allowing further repeats).
                    dp[i][j] = dp[i][j + 2] or (first_match and dp[i + 1][j])
                else:
                    dp[i][j] = first_match and dp[i + 1][j + 1]

        return dp[0][0]

    def isMatchRecursive(self, s: str, p: str) -> bool:
        """
        Top-down memoized recursive solution, provided for comparison.
        Same time/space complexity as the DP version, but often easier
        to reason about.
        """

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)

            first_match = i < len(s) and p[j] in (s[i], '.')

            if j + 1 < len(p) and p[j + 1] == '*':
                return dp(i, j + 2) or (first_match and dp(i + 1, j))
            else:
                return first_match and dp(i + 1, j + 1)

        return dp(0, 0)


def run_tests():
    sol = Solution()
    test_cases = [
        ("aa", "a", False),
        ("aa", "a*", True),
        ("ab", ".*", True),
        ("aab", "c*a*b", True),
        ("mississippi", "mis*is*p*.", False),
        ("", "", True),
        ("", "a*", True),
        ("", ".*", True),
        ("ab", ".*c", False),
        ("aaa", "a*a", True),
        ("aaa", "ab*a*c*a", True),
    ]

    all_passed = True
    for s, p, expected in test_cases:
        result_dp = sol.isMatch(s, p)
        result_rec = sol.isMatchRecursive(s, p)
        status = "PASS" if result_dp == expected else "FAIL"
        if result_dp != expected or result_rec != expected:
            all_passed = False
        print(f"[{status}] isMatch(s={s!r}, p={p!r}) = {result_dp} "
            f"(expected {expected}) | recursive = {result_rec}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()