"""
7. Reverse Integer
https://leetcode.com/problems/reverse-integer/

Given a signed 32-bit integer x, return x with its digits reversed. If
reversing x causes the value to go outside the signed 32-bit integer range
[-2^31, 2^31 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers
(signed or unsigned).

Example 1:
    Input: x = 123
    Output: 321

Example 2:
    Input: x = -123
    Output: -321

Example 3:
    Input: x = 120
    Output: 21

Constraints:
    -2^31 <= x <= 2^31 - 1
"""


class Solution:
    def reverse(self, x: int) -> int:
        """
        Pop digits off the end of x one at a time and push them onto a
        new number, building the reversed integer digit by digit -
        checking for 32-bit overflow before each push.

        Time Complexity:  O(log10(x)) - one iteration per digit in x.
        Space Complexity: O(1)        - only a constant amount of extra
                           space is used regardless of input size.
        """
        INT_MAX = 2**31 - 1   # 2147483647
        INT_MIN = -2**31      # -2147483648

        result = 0
        remaining = abs(x)
        sign = -1 if x < 0 else 1

        while remaining != 0:
            digit = remaining % 10
            remaining //= 10

            # Check for overflow/underflow before actually updating result.
            if result > (INT_MAX - digit) // 10:
                return 0

            result = result * 10 + digit

        result *= sign

        if result < INT_MIN or result > INT_MAX:
            return 0

        return result


if __name__ == "__main__":
    solution = Solution()

    # Example 1
    print(solution.reverse(123))          # 321

    # Example 2
    print(solution.reverse(-123))         # -321

    # Example 3
    print(solution.reverse(120))          # 21

    # Overflow cases
    print(solution.reverse(1534236469))   # 0 (would overflow 32-bit range)
    print(solution.reverse(-2147483648))  # 0 (reversed value overflows)

    # Edge cases
    print(solution.reverse(0))            # 0