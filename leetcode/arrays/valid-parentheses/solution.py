"""
LeetCode 20 - Valid Parentheses
https://leetcode.com/problems/valid-parentheses/

Given a string s containing just the characters '(', ')', '{', '}', '[',
']', determine if the input string is valid.

An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same
       type.

Example 1:
    Input: s = "()"
    Output: True

Example 2:
    Input: s = "()[]{}"
    Output: True

Example 3:
    Input: s = "(]"
    Output: False

Example 4:
    Input: s = "([])"
    Output: True

Constraints:
    1 <= s.length <= 10^4
    s consists of parentheses only '()[]{}'.
"""


class Solution:
    def isValid(self, s: str) -> bool:
        """
        Stack-based solution.

        Walk through the string; push every opening bracket onto a
        stack. When a closing bracket is seen, it must match the bracket
        on top of the stack (the most recently opened, still-unclosed
        one) - if the stack is empty or the top doesn't match, the string
        is invalid. At the end, the string is valid only if the stack is
        completely empty (every opened bracket got closed).

        Time Complexity:  O(n) - single pass over the string
        Space Complexity: O(n) - worst case (all opening brackets) the
                           stack holds every character
        """
        matching = {
            ")": "(",
            "]": "[",
            "}": "{",
        }

        stack = []
        for char in s:
            if char in matching:
                if not stack or stack[-1] != matching[char]:
                    return False
                stack.pop()
            else:
                stack.append(char)

        return not stack

    def isValidReplace(self, s: str) -> bool:
        """
        Alternative solution: repeatedly remove innermost matched pairs
        ("()", "[]", "{}") from the string until no more removals are
        possible. The string is valid if and only if it reduces down to
        empty. Included for comparison - conceptually simple, but far
        less efficient.

        Time Complexity:  O(n^2) - up to n/2 removal passes, each
                           potentially scanning/rebuilding an O(n) string
        Space Complexity: O(n) - new strings created on each replacement
        """
        prev_length = -1
        while len(s) != prev_length:
            prev_length = len(s)
            s = s.replace("()", "").replace("[]", "").replace("{}", "")

        return s == ""


def run_tests():
    sol = Solution()
    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([])", True),
        ("([)]", False),
        ("", True),
        ("(", False),
        ("]", False),
        ("{[]}", True),
        ("((()))", True),
        ("(()", False),
        ("()()()", True),
    ]

    all_passed = True
    for s, expected in test_cases:
        result_stack = sol.isValid(s)
        result_replace = sol.isValidReplace(s)
        status = "PASS" if result_stack == expected else "FAIL"
        if result_stack != expected or result_replace != expected:
            all_passed = False
        print(f"[{status}] isValid({s!r}) = {result_stack} "
              f"(expected {expected}) | replace method = {result_replace}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()