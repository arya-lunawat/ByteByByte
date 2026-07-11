"""
LeetCode 9 - Palindrome Number
https://leetcode.com/problems/palindrome-number/description/

Given an integer x, return True if x is a palindrome, and False otherwise.

Example 1:
    Input: x = 121
    Output: True

Example 2:
    Input: x = -121
    Output: False
    Explanation: From left to right, it reads -121. From right to left,
    it becomes 121-. Therefore it is not a palindrome.

Example 3:
    Input: x = 10
    Output: False
    Explanation: Reads 01 from right to left. Therefore it is not a palindrome.

Constraints:
    -2^31 <= x <= 2^31 - 1

Follow up: Could you solve it without converting the integer to a string?
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        O(1) extra space solution that avoids full string conversion by
        reversing only half of the number and comparing the two halves.

        Time Complexity:  O(log10(x)) - number of digits in x
        Space Complexity: O(1)
        """
        # Negative numbers are never palindromes (leading '-' has no match).
        # Numbers ending in 0 (except 0 itself) can't be palindromes either,
        # since a palindrome can't start with 0.
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reverted_half = 0
        while x > reverted_half:
            reverted_half = reverted_half * 10 + x % 10
            x //= 10

        # For even digit counts, x == reverted_half.
        # For odd digit counts, the middle digit is discarded by
        # dividing reverted_half by 10 (e.g. 12321 -> x=12, reverted_half=123).
        return x == reverted_half or x == reverted_half // 10

    def isPalindromeString(self, x: int) -> bool:
        """
        Simpler O(n) solution using string conversion, provided for
        comparison / readability.
        """
        if x < 0:
            return False
        s = str(x)
        return s == s[::-1]


def run_tests():
    sol = Solution()
    test_cases = [
        (121, True),
        (-121, False),
        (10, False),
        (0, True),
        (1, True),
        (12321, True),
        (123321, True),
        (1221, True),
        (100, False),
        (2**31 - 1, False),
    ]

    all_passed = True
    for x, expected in test_cases:
        result = sol.isPalindrome(x)
        result_str = sol.isPalindromeString(x)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"[{status}] isPalindrome({x}) = {result} (expected {expected}) "
            f"| string method = {result_str}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()