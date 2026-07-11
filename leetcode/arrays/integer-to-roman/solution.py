"""
LeetCode 12 - Integer to Roman
https://leetcode.com/problems/integer-to-roman/

Seven different symbols represent Roman numerals with the following
values:

    Symbol  Value
    I       1
    V       5
    X       10
    L       50
    C       100
    D       500
    M       1000

Roman numerals are formed by appending the conversions of decimal place
values from highest to lowest. Converting a decimal place value into a
Roman numeral has the following rules:

    - If the value does not start with 4 or 9, select the symbol of the
      maximal value that can be subtracted from the input, append that
      symbol to the result, subtract its value, and repeat this process
      until the input becomes 0.
    - If the value starts with 4 or 9, use the "subtractive" form,
      representing one symbol subtracted from the following symbol, e.g.
      4 is 1 (I) less than 5 (V): "IV"; 9 is 1 (I) less than 10 (X): "IX".
      Only powers of 10 (I, X, C, M) can be used as the subtractive
      value.

Given an integer, convert it to a Roman numeral.

Example 1:
    Input: num = 3749
    Output: "MMMDCCXLIX"
    Explanation: 3000 = MMM, 700 = DCC, 40 = XL, 9 = IX

Example 2:
    Input: num = 58
    Output: "LVIII"
    Explanation: 50 = L, 8 = VIII

Example 3:
    Input: num = 1994
    Output: "MCMXCIV"
    Explanation: 1000 = M, 900 = CM, 90 = XC, 4 = IV

Constraints:
    1 <= num <= 3999
"""


class Solution:
    def intToRoman(self, num: int) -> str:
        """
        Greedy solution using a value-symbol table that already encodes
        the subtractive forms (4, 9, 40, 90, 400, 900) alongside the
        standard values. Repeatedly subtract the largest value that fits
        and append its symbol.

        Time Complexity:  O(1) - at most 13 iterations regardless of num
                           (bounded by num <= 3999)
        Space Complexity: O(1) - fixed-size table, output length is bounded
        """
        value_symbols = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        result = []
        for value, symbol in value_symbols:
            if num == 0:
                break
            count, num = divmod(num, value)
            if count:
                result.append(symbol * count)

        return "".join(result)

    def intToRomanDigitByDigit(self, num: int) -> str:
        """
        Alternative solution that converts each decimal digit (thousands,
        hundreds, tens, ones) independently using precomputed lookup
        tables for each place value. Provided for comparison; a common
        way to express the same idea without a subtraction loop.

        Time Complexity:  O(1) - always processes exactly 4 digit places
        Space Complexity: O(1)
        """
        thousands = ["", "M", "MM", "MMM"]
        hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

        return (
            thousands[num // 1000]
            + hundreds[(num % 1000) // 100]
            + tens[(num % 100) // 10]
            + ones[num % 10]
        )


def run_tests():
    sol = Solution()
    test_cases = [
        (3749, "MMMDCCXLIX"),
        (58, "LVIII"),
        (1994, "MCMXCIV"),
        (1, "I"),
        (4, "IV"),
        (9, "IX"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (3999, "MMMCMXCIX"),
        (2024, "MMXXIV"),
    ]

    all_passed = True
    for num, expected in test_cases:
        result_greedy = sol.intToRoman(num)
        result_digit = sol.intToRomanDigitByDigit(num)
        status = "PASS" if result_greedy == expected else "FAIL"
        if result_greedy != expected or result_digit != expected:
            all_passed = False
        print(f"[{status}] intToRoman({num}) = {result_greedy!r} "
            f"(expected {expected!r}) | digit-by-digit = {result_digit!r}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()