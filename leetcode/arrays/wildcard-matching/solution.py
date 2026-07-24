"""
LeetCode 44 - Wildcard Matching
https://leetcode.com/problems/wildcard-matching/

Given an input string s and a pattern p, implement wildcard pattern
matching with support for '?' and '*' where:
    '?' Matches any single character.
    '*' Matches any sequence of characters (including the empty
        sequence).

The matching should cover the entire input string (not partial).
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Plain recursion, no memoization.

    Compare s and p position by position:
      - If p[j] is '?', or s[i] == p[j], both characters match --
        advance both pointers and recurse.
      - If p[j] is '*', it can match either the empty sequence (skip
        the '*' in the pattern, keep i) or one more character of s
        (keep the '*' in the pattern in case it needs to consume more,
        advance i) -- try both branches, succeed if either does.
      - Otherwise, this is a mismatch -- fail.
      - Base cases: if we reach the end of the pattern, we succeed only
        if we've also reached the end of s. If we reach the end of s
        but not the pattern, we succeed only if all remaining pattern
        characters are '*' (since '*' can match empty).

    Without memoization, overlapping subproblems (the same (i, j) pair
    reached via different paths, which happens a lot with '*') get
    recomputed repeatedly, leading to exponential blowup on adversarial
    inputs like s = "aaaa...a", p = "a*a*a*...*".

    Time:  O(2^(m+n)) worst case (m = len(s), n = len(p)) -- each '*'
           can branch into two recursive calls, and these branches
           compound across the length of the strings.
    Space: O(m + n) for the recursion stack depth in the worst case.
    """

    def isMatch(self, s: str, p: str) -> bool:
        def match(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)

            if p[j] == "*":
                # Try: '*' matches empty (advance j only), or
                # '*' consumes one more char of s (advance i only).
                return (i < len(s) and match(i + 1, j)) or match(i, j + 1)

            if i < len(s) and (p[j] == "?" or p[j] == s[i]):
                return match(i + 1, j + 1)

            return False

        return match(0, 0)


class Solution:
    """
    Approach: Bottom-up dynamic programming.

    Build a 2D table dp[i][j] = True if s[:i] matches p[:j] (using
    prefixes of length i and j respectively). This directly reuses
    overlapping subproblems instead of recomputing them.

    Base case: dp[0][0] = True (empty matches empty). dp[0][j] = True
    only if p[:j] is all '*' characters, since only '*' can match an
    empty string.

    Transitions, for i >= 1, j >= 1:
      - If p[j-1] == '?' or p[j-1] == s[i-1]: this pair of characters
        matches directly, so dp[i][j] = dp[i-1][j-1] (whatever the
        strings looked like one character back).
      - If p[j-1] == '*': it can either match the empty sequence
        (dp[i][j-1] -- pattern consumes the '*' without using any of
        s) or match one more character of s while still being
        available to match further characters (dp[i-1][j] -- s
        advances but the '*' stays "active" in the pattern). If either
        is True, dp[i][j] = True.
      - Otherwise: mismatch, dp[i][j] = False.

    Answer is dp[len(s)][len(p)].

    Time:  O(m * n) -- one entry computed per (i, j) pair, O(1) work
           each.
    Space: O(m * n) for the DP table.
    """

    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp: List[List[bool]] = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True

        # Row 0: only patterns made entirely of '*' can match an empty s.
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[0][j] = dp[0][j - 1]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == "?" or p[j - 1] == s[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                elif p[j - 1] == "*":
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
                # else: dp[i][j] stays False (mismatch)

        return dp[m][n]


if __name__ == "__main__":
    tests = [
        ("aa", "a", False),
        ("aa", "*", True),
        ("cb", "?a", False),
        ("adceb", "*a*b", True),
        ("acdcb", "a*c?b", False),
        ("", "", True),
        ("", "*", True),
        ("", "a*", False),
        ("abc", "abc", True),
        ("mississippi", "m??*ss*?i*pi", False),
        ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*a*", True),
    ]

    for s, p, expected in tests:
        r_opt = Solution().isMatch(s, p)
        s_opt = "PASS" if r_opt == expected else "FAIL"

        # Skip the pathological worst-case string for brute force (too slow);
        # verify it separately with the DP-only note below.
        if len(s) + len(p) <= 40:
            r_brute = SolutionBruteForce().isMatch(s, p)
            s_brute = "PASS" if r_brute == expected else "FAIL"
            print(
                f"isMatch({s!r}, {p!r}) -> brute={r_brute} [{s_brute}], "
                f"optimal={r_opt} [{s_opt}], expected={expected}"
            )
        else:
            print(
                f"isMatch({s!r}, {p!r}) -> brute=SKIPPED (exponential blowup), "
                f"optimal={r_opt} [{s_opt}], expected={expected}"
            )