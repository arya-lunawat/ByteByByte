"""
LeetCode 29 - Divide Two Integers
https://leetcode.com/problems/divide-two-integers/

Given two integers dividend and divisor, divide them WITHOUT using
multiplication, division, or the mod operator. Truncate toward zero.
Clamp the result to the signed 32-bit integer range [-2^31, 2^31 - 1].
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Repeated subtraction.

    Keep subtracting the absolute divisor from the absolute dividend,
    counting how many times we can do it before the remainder is
    smaller than the divisor.

    Time:  O(dividend / divisor)  -> can TLE on large inputs
           (e.g. dividend = 2^31 - 1, divisor = 1 takes ~2 billion steps)
    Space: O(1)
    """

    def divide(self, dividend: int, divisor: int) -> int:
        INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1

        negative = (dividend < 0) != (divisor < 0)
        a, b = abs(dividend), abs(divisor)

        quotient = 0
        while a >= b:
            a -= b
            quotient += 1

        quotient = -quotient if negative else quotient
        return max(INT_MIN, min(INT_MAX, quotient))


class Solution:
    """
    Approach: Bit-shift doubling (exponential/repeated subtraction).

    Instead of subtracting the divisor one copy at a time, subtract the
    largest possible multiple of the divisor (a power-of-two multiple)
    in each step. We build that multiple by doubling it (left shift)
    while it still fits inside the remaining dividend, then subtract it
    and add the corresponding power of two to the quotient. Repeat on
    what's left.

    This mirrors how long division works in binary and avoids using
    '*', '/', or '%'.

    Time:  O(log^2(dividend)) in the worst case
           (outer loop runs O(log n) times, inner doubling loop O(log n) times)
    Space: O(1)
    """

    def divide(self, dividend: int, divisor: int) -> int:
        INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1

        # Overflow edge case: -2^31 / -1 = 2^31, which doesn't fit in 32 bits.
        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        negative = (dividend < 0) != (divisor < 0)
        a, b = abs(dividend), abs(divisor)

        quotient = 0
        while a >= b:
            temp, multiple = b, 1
            # Double temp (and multiple) as long as it still fits in a.
            while temp + temp <= a:
                temp += temp        # temp <<= 1
                multiple += multiple  # multiple <<= 1
            a -= temp
            quotient += multiple

        quotient = -quotient if negative else quotient
        return max(INT_MIN, min(INT_MAX, quotient))


if __name__ == "__main__":
    tests: List[tuple] = [
        (10, 3, 3),
        (7, -3, -2),
        (0, 1, 0),
        (1, 1, 1),
        (-2147483648, -1, 2147483647),  # overflow clamp
        (-2147483648, 1, -2147483648),
        (1, -1, -1),
    ]

    for dividend, divisor, expected in tests:
        got_optimal = Solution().divide(dividend, divisor)
        got_brute = SolutionBruteForce().divide(dividend, divisor)
        status_opt = "PASS" if got_optimal == expected else "FAIL"
        status_brute = "PASS" if got_brute == expected else "FAIL"
        print(
            f"divide({dividend}, {divisor}) -> optimal={got_optimal} [{status_opt}], "
            f"brute={got_brute} [{status_brute}], expected={expected}"
        )