"""
LeetCode 17 - Letter Combinations of a Phone Number
https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/

Given a string containing digits from 2-9 inclusive, return all possible
letter combinations that the number could represent. Return the answer
in any order.

A mapping of digits to letters (just like on the telephone buttons) is
given below. Note that 1 does not map to any letters.

    2: "abc"    3: "def"    4: "ghi"    5: "jkl"
    6: "mno"    7: "pqrs"   8: "tuv"    9: "wxyz"

Example 1:
    Input: digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
    Input: digits = ""
    Output: []

Example 3:
    Input: digits = "2"
    Output: ["a","b","c"]

Constraints:
    0 <= digits.length <= 4
    digits[i] is a digit in the range ['2', '9'].
"""


class Solution:
    DIGIT_TO_LETTERS = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    def letterCombinations(self, digits: str) -> list[str]:
        """
        Backtracking (DFS) solution.

        Build combinations one digit at a time: for each digit, try every
        letter it could map to, append it to the current path, recurse
        into the next digit, then remove it (backtrack) before trying the
        next letter. When the path length matches the number of digits,
        it's a complete combination.

        Time Complexity:  O(4^n * n) where n is len(digits) - up to 4
                           letters per digit (digits 7 and 9 have 4
                           letters each), and building/copying each
                           combination of length n costs O(n)
        Space Complexity: O(n) for the recursion depth and current path,
                           not counting the output
        """
        if not digits:
            return []

        result = []
        path = []

        def backtrack(index: int) -> None:
            if index == len(digits):
                result.append("".join(path))
                return

            letters = self.DIGIT_TO_LETTERS[digits[index]]
            for letter in letters:
                path.append(letter)
                backtrack(index + 1)
                path.pop()

        backtrack(0)
        return result

    def letterCombinationsIterative(self, digits: str) -> list[str]:
        """
        Alternative solution: iterative BFS-style build-up. Start with a
        list containing just the empty string, and for each digit,
        expand every existing combination by each letter that digit maps
        to, producing the next "layer" of combinations.

        Time Complexity:  O(4^n * n) - same bound as backtracking
        Space Complexity: O(4^n * n) for the intermediate combination
                           lists (comparable to the output size at each
                           step)
        """
        if not digits:
            return []

        combinations = [""]
        for digit in digits:
            letters = self.DIGIT_TO_LETTERS[digit]
            combinations = [
                combo + letter
                for combo in combinations
                for letter in letters
            ]

        return combinations


def run_tests():
    sol = Solution()
    test_cases = [
        ("23", ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
        ("", []),
        ("2", ["a", "b", "c"]),
        ("7", ["p", "q", "r", "s"]),
        ("79", ["pw", "px", "py", "pz", "qw", "qx", "qy", "qz",
                "rw", "rx", "ry", "rz", "sw", "sx", "sy", "sz"]),
    ]

    all_passed = True
    for digits, expected in test_cases:
        result_backtrack = sorted(sol.letterCombinations(digits))
        result_iterative = sorted(sol.letterCombinationsIterative(digits))
        expected_sorted = sorted(expected)
        status = "PASS" if result_backtrack == expected_sorted else "FAIL"
        if result_backtrack != expected_sorted or result_iterative != expected_sorted:
            all_passed = False
        print(f"[{status}] letterCombinations({digits!r}) has "
              f"{len(result_backtrack)} combos (expected {len(expected_sorted)}) "
              f"| backtrack == iterative: {result_backtrack == result_iterative}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()