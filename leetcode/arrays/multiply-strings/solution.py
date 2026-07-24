"""
LeetCode 43 - Multiply Strings
https://leetcode.com/problems/multiply-strings/

Given two non-negative integers num1 and num2 represented as strings,
return the product of num1 and num2, also represented as a string.

Note: You must not use any built-in BigInteger library or convert the
inputs to integers directly.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Convert to native ints, multiply, convert back.

    This is exactly what the problem statement says NOT to do -- it
    leans entirely on Python's arbitrary-precision int type to do the
    actual multiplication, rather than implementing grade-school
    multiplication by hand. Included purely as a baseline / sanity
    check for correctness, not as a legitimate solution.

    Time:  Technically depends on Python's big-int multiplication
           algorithm (Karatsuba-ish for CPython), but conceptually this
           sidesteps the problem entirely rather than measuring
           anything meaningful about the intended approach.
    Space: O(len(num1) + len(num2)) for the string conversions.
    """

    def multiply(self, num1: str, num2: str) -> str:
        return str(int(num1) * int(num2))


class Solution:
    """
    Approach: Grade-school digit-by-digit multiplication with an
    array of partial results (no built-in big-int arithmetic).

    Mirrors how you'd multiply two numbers by hand on paper:

    For two numbers with lengths m and n, the product has at most
    m + n digits. Allocate a result array `product` of size m + n,
    all zeros, where `product[i]` will hold a single decimal digit
    once fully summed (after carrying).

    For every pair of digits num1[i] (from the right, position i) and
    num2[j] (from the right, position j), their contribution lands at
    combined position i + j in the product -- more precisely, since
    we're indexing from the left in the string, digit num1[i] * 10^p1
    times digit num2[j] * 10^p2 contributes to positions
    (p1 + p2) and (p1 + p2 + 1) in the result array (least-significant
    digit of that partial product goes to the "ones-ish" slot, the
    carry-out goes one slot to the left). We ADD this partial product
    into product[i + j + 1] (and let overflow ripple into
    product[i + j] via the addition itself), rather than assigning,
    since multiple digit-pairs can contribute to the same result
    position.

    After all digit pairs are processed, `product` may contain values
    greater than 9 in some slots (unresolved carries) -- walk it once
    from right to left, propagating carry-over into the next slot to
    the left, same as manually carrying when adding a column of
    numbers.

    Finally, convert the digit array to a string, skipping any leading
    zeros (but keeping at least one digit for the "0" result), and
    handle the "either input is 0" case up front as a shortcut.

    Time:  O(m * n) -- every pair of digits (one from each number) is
           visited exactly once to compute and accumulate its partial
           product.
    Space: O(m + n) -- the result digit array.
    """

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        product = [0] * (m + n)

        # Iterate right-to-left over both numbers (least significant
        # digit first), same as doing long multiplication by hand.
        for i in range(m - 1, -1, -1):
            digit1 = ord(num1[i]) - ord("0")
            for j in range(n - 1, -1, -1):
                digit2 = ord(num2[j]) - ord("0")

                # This digit pair's product contributes to two adjacent
                # positions in the result: the "low" digit lands at
                # i + j + 1, and any carry bumps into i + j.
                low_pos = i + j + 1
                high_pos = i + j

                total = digit1 * digit2 + product[low_pos]
                product[low_pos] = total % 10
                product[high_pos] += total // 10

        # Convert digits to string, dropping leading zeros.
        start = 0
        while start < len(product) - 1 and product[start] == 0:
            start += 1

        return "".join(str(d) for d in product[start:])


if __name__ == "__main__":
    tests = [
        ("2", "3", "6"),
        ("123", "456", "56088"),
        ("0", "0", "0"),
        ("0", "52", "0"),
        ("999", "999", "998001"),
        ("1", "1", "1"),
        ("123456789", "987654321", "121932631112635269"),
        ("9", "9", "81"),
    ]

    for num1, num2, expected in tests:
        r_brute = SolutionBruteForce().multiply(num1, num2)
        r_opt = Solution().multiply(num1, num2)
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"multiply({num1!r}, {num2!r}) -> "
            f"brute={r_brute!r} [{s_brute}], optimal={r_opt!r} [{s_opt}], expected={expected!r}"
        )