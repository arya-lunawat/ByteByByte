"""
8. String to Integer (atoi)
https://leetcode.com/problems/string-to-integer-atoi/

Implement the myAtoi(string s) function, which converts a string to a
32-bit signed integer.

The algorithm for myAtoi(string s) is as follows:
    1. Whitespace: Ignore any leading whitespace (" ").
    2. Signedness: Determine the sign by checking if the next character is
       '-' or '+', assuming positivity if neither present.
    3. Conversion: Read the integer by skipping leading zeros until a
       non-digit character is encountered or the end of the string is
       reached. If no digits were read, then the result is 0.
    4. Rounding: If the integer is out of the 32-bit signed integer range
       [-2^31, 2^31 - 1], then round the integer to remain in the range.
       Specifically, integers less than -2^31 should be rounded to -2^31,
       and integers greater than 2^31 - 1 should be rounded to 2^31 - 1.

Return the integer as the final result.

Example 1:
    Input: s = "42"
    Output: 42

Example 2:
    Input: s = " -042"
    Output: -42

Example 3:
    Input: s = "1337c0d3"
    Output: 1337

Example 4:
    Input: s = "0-1"
    Output: 0

Example 5:
    Input: s = "words and 987"
    Output: 0

Constraints:
    0 <= s.length <= 200
    s consists of English letters (lower-case and upper-case), digits
    (0-9), ' ', '+', '-', and '.'.
"""


class Solution:
    def myAtoi(self, s: str) -> int:
        """
        Simulate the atoi algorithm step by step, as described above:
        skip leading whitespace, read an optional sign, read consecutive
        digits, then clamp the result to the 32-bit signed integer range.

        Time Complexity:  O(n) - each character in s is visited at most
                           once.
        Space Complexity: O(1) - only a constant amount of extra space is
                           used regardless of input size.
        """
        INT_MAX = 2**31 - 1   # 2147483647
        INT_MIN = -2**31      # -2147483648

        i = 0
        n = len(s)

        # 1. Skip leading whitespace.
        while i < n and s[i] == " ":
            i += 1

        if i == n:
            return 0

        # 2. Determine the sign, if any.
        sign = 1
        if s[i] == "+" or s[i] == "-":
            if s[i] == "-":
                sign = -1
            i += 1

        # 3. Read consecutive digits, skipping leading zeros naturally
        #    (building the number arithmetically rather than tracking
        #    zero-skipping separately).
        result = 0
        while i < n and s[i].isdigit():
            digit = int(s[i])

            # 4. Clamp to the 32-bit range as soon as we would overflow,
            #    rather than waiting until after building the full number
            #    (mirrors the overflow-safe technique used for languages
            #    with fixed-width integers).
            if result > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN

            result = result * 10 + digit
            i += 1

        return sign * result


if __name__ == "__main__":
    solution = Solution()

    # Example 1
    print(solution.myAtoi("42"))              # 42

    # Example 2
    print(solution.myAtoi(" -042"))           # -42

    # Example 3
    print(solution.myAtoi("1337c0d3"))        # 1337

    # Example 4
    print(solution.myAtoi("0-1"))             # 0

    # Example 5
    print(solution.myAtoi("words and 987"))   # 0

    # Overflow / edge cases
    print(solution.myAtoi("91283472332"))     # 2147483647 (clamped to INT_MAX)
    print(solution.myAtoi("-91283472332"))    # -2147483648 (clamped to INT_MIN)
    print(solution.myAtoi(""))                # 0
    print(solution.myAtoi("   "))             # 0
    print(solution.myAtoi("+-12"))            # 0 (invalid sign sequence)
    print(solution.myAtoi("  +  413"))        # 0 (space between sign and digits)