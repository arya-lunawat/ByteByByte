"""
LeetCode 32 - Longest Valid Parentheses
https://leetcode.com/problems/longest-valid-parentheses/

Given a string containing just the characters '(' and ')', return the
length of the longest valid (well-formed) parentheses substring.

Example:
    s = ")()())"  ->  4   (the substring "()()" starting at index 1)
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Check every substring for validity.

    For every pair of start/end indices, extract the substring and run
    a standard "balanced parentheses" check on it (a counter that must
    never go negative and must end at zero). Track the longest one that
    passes.

    Time:  O(n^3) -- O(n^2) substrings, O(n) to validate each
    Space: O(n)   -- for the substring / validation itself
    """

    def longestValidParentheses(self, s: str) -> int:
        n = len(s)
        best = 0

        def is_valid(sub: str) -> bool:
            balance = 0
            for ch in sub:
                balance += 1 if ch == "(" else -1
                if balance < 0:
                    return False
            return balance == 0

        for i in range(n):
            for j in range(i + 2, n + 1, 2):  # valid substrings have even length
                if is_valid(s[i:j]):
                    best = max(best, j - i)

        return best


class SolutionStack:
    """
    Approach: Index stack.

    Push -1 as a sentinel "base" index onto the stack. Then for each
    character:
      - '(' -> push its index (a candidate opening bracket).
      - ')' -> pop the stack (closing out the top opening bracket, if
        any). If the stack becomes empty, this ')' has no match at all,
        so push its own index as the new base for future substrings.
        Otherwise, the current valid run's length is
        `i - stack[-1]` (current index minus the new top of stack,
        which marks the boundary just before the current valid run).

    The sentinel handles the "nothing has matched yet" case cleanly,
    and re-pushing an unmatched ')' index resets the base the same way.

    Time:  O(n) -- each index is pushed and popped at most once
    Space: O(n) -- the stack, worst case all '(' or all unmatched ')'
    """

    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]  # sentinel base index
        best = 0

        for i, ch in enumerate(s):
            if ch == "(":
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)  # new base: this ')' is unmatched
                else:
                    best = max(best, i - stack[-1])

        return best


class Solution:
    """
    Approach: Two-pass counters (O(1) extra space).

    Pass 1 (left-to-right): track counts of '(' seen (`open`) and ')'
    seen (`close`).
      - Whenever open == close, we have a balanced run of length
        2 * close, so update the answer.
      - Whenever close > open, this position can never be part of a
        valid run starting from before it (too many closes) -- reset
        both counters to 0 and keep scanning.

    This single pass under-counts whenever '(' outnumbers ')' in a run
    (e.g. "((()" never triggers a close > open reset, so the trailing
    valid "()" never gets isolated and measured). Pass 2 fixes this by
    scanning right-to-left with the roles of '(' and ')' swapped,
    resetting whenever open > close. Together, each pass catches the
    failure mode the other one misses (excess ')' vs. excess '(').

    Time:  O(n) -- two linear passes over s
    Space: O(1) -- just a handful of counters
    """

    def longestValidParentheses(self, s: str) -> int:
        best = 0

        # Left-to-right: catches excess ')' by resetting when close > open
        open_count = close_count = 0
        for ch in s:
            if ch == "(":
                open_count += 1
            else:
                close_count += 1
            if open_count == close_count:
                best = max(best, 2 * close_count)
            elif close_count > open_count:
                open_count = close_count = 0

        # Right-to-left: catches excess '(' by resetting when open > close
        open_count = close_count = 0
        for ch in reversed(s):
            if ch == "(":
                open_count += 1
            else:
                close_count += 1
            if open_count == close_count:
                best = max(best, 2 * open_count)
            elif open_count > close_count:
                open_count = close_count = 0

        return best


if __name__ == "__main__":
    tests = [
        ("(()", 2),
        (")()())", 4),
        ("", 0),
        ("()(()", 2),
        ("()(())", 6),
        ("((()))", 6),
        (")(", 0),
        ("()()", 4),
        ("(((((", 0),
        (")))))", 0),
        ("(()())", 6),
    ]

    for s, expected in tests:
        r_brute = SolutionBruteForce().longestValidParentheses(s)
        r_stack = SolutionStack().longestValidParentheses(s)
        r_opt = Solution().longestValidParentheses(s)

        statuses = [
            "PASS" if r == expected else "FAIL"
            for r in (r_brute, r_stack, r_opt)
        ]
        print(
            f"longestValidParentheses({s!r}) -> "
            f"brute={r_brute} [{statuses[0]}], "
            f"stack={r_stack} [{statuses[1]}], "
            f"optimal={r_opt} [{statuses[2]}], "
            f"expected={expected}"
        )