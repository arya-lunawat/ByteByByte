"""
LeetCode 13 - Roman to Integer
https://leetcode.com/problems/roman-to-integer/description/

Roman numerals are represented by seven different symbols:

    Symbol  Value
    I       1
    V       5
    X       10
    L       50
    C       100
    D       500
    M       1000

Roman numerals are usually written largest to smallest from left to
right, e.g. 2 is written as "II" (two ones), 27 as "XXVII".

Six instances use a subtractive form:
    - I before V (5) or X (10) -> 4 and 9
    - X before L (50) or C (100) -> 40 and 90
    - C before D (500) or M (1000) -> 400 and 900

Given a roman numeral, convert it to an integer.

Example 1:
    Input: s = "III"
    Output: 3
    Explanation: III = 3.

Example 2:
    Input: s = "LVIII"
    Output: 58
    Explanation: L = 50, V = 5, III = 3.

Example 3:
    Input: s = "MCMXCIV"
    Output: 1994
    Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.

Constraints:
    1 <= s.length <= 15
    s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
    It is guaranteed that s is a valid roman numeral in the range
    [1, 3999].
"""


class Solution:
    def romanToInt(self, s: str) -> int:
        """
        Left-to-right scan comparing each symbol's value to the value of
        the symbol right after it.

        The key insight: in the subtractive form (e.g. "IV"), the smaller
        symbol comes before a strictly larger one. So instead of
        special-casing pairs like "IV" or "CM", we can just look one
        symbol ahead: if the current symbol's value is less than the
        next symbol's value, we're in a subtractive pair, so we subtract
        the current value; otherwise we add it.

        Time Complexity:  O(n) - single pass over the string
        Space Complexity: O(1) - fixed-size lookup table
        """
        values = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        total = 0
        n = len(s)
        for i in range(n):
            current = values[s[i]]
            if i + 1 < n and current < values[s[i + 1]]:
                total -= current
            else:
                total += current

        return total

    def romanToIntReplace(self, s: str) -> int:
        """
        Alternative solution: replace every subtractive pair with a
        placeholder-free equivalent value string wouldn't quite work
        directly, so instead we substitute each subtractive pair with a
        single "virtual" symbol contributing the correct net value, then
        sum plain symbol values. Implemented here via string replacement
        of the six known subtractive pairs before summing.

        Time Complexity:  O(n) - a handful of fixed replacements plus a
                           single pass to sum
        Space Complexity: O(n) - due to string replacement creating new
                           strings
        """
        values = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        replacements = {
            "IV": "IIII",
            "IX": "VIIII",
            "XL": "XXXX",
            "XC": "LXXXX",
            "CD": "CCCC",
            "CM": "DCCCC",
        }

        for pair, expansion in replacements.items():
            s = s.replace(pair, expansion)

        return sum(values[ch] for ch in s)


def run_tests():
    sol = Solution()
    test_cases = [
        ("III", 3),
        ("LVIII", 58),
        ("MCMXCIV", 1994),
        ("IV", 4),
        ("IX", 9),
        ("XL", 40),
        ("XC", 90),
        ("CD", 400),
        ("CM", 900),
        ("MMMCMXCIX", 3999),
        ("I", 1),
        ("MMXXIV", 2024),
    ]

    all_passed = True
    for s, expected in test_cases:
        result_scan = sol.romanToInt(s)
        result_replace = sol.romanToIntReplace(s)
        status = "PASS" if result_scan == expected else "FAIL"
        if result_scan != expected or result_replace != expected:
            all_passed = False
        print(f"[{status}] romanToInt({s!r}) = {result_scan} "
              f"(expected {expected}) | replace method = {result_replace}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()