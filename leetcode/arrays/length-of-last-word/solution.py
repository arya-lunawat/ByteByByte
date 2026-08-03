"""
58. Length of Last Word
https://leetcode.com/problems/length-of-last-word/

Given a string s consisting of words and spaces, return the length of
the last word in the string.

A word is a maximal substring consisting of non-space characters
only.

Example:
    Input:  s = "Hello World"
    Output: 5
    Explanation: The last word is "World" with length 5.

    Input:  s = "   fly me   to   the moon  "
    Output: 4
    Explanation: The last word is "moon" with length 4.

    Input:  s = "luffy is still joyboy"
    Output: 6
    Explanation: The last word is "joyboy" with length 6.

Constraints:
    1 <= s.length <= 10^4
    s consists of only English letters and spaces ' '.
    There will be at least one word in s.
"""


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        """
        Approach 1: Built-in split.

        Python's str.split() with no argument already treats runs of
        whitespace as a single separator and discards leading/trailing
        whitespace entirely, so splitting the string and taking the
        length of the final piece handles all of the trailing-spaces
        and multiple-spaces edge cases for free.

        Time:  O(n) -- split scans the whole string once.
        Space: O(n) -- split builds a list of all the words.
        """
        words = s.split()
        return len(words[-1])

    def lengthOfLastWordTwoPointer(self, s: str) -> int:
        """
        Approach 2: Two-pointer scan from the end, no splitting.

        Walk backward from the end of the string:
          1. Skip over any trailing spaces to find the last
             non-space character (the end of the last word).
          2. Continue walking backward while characters are
             non-space, counting them, to find the start of that word.
        Stop as soon as a space is hit (or the start of the string is
        reached) -- everything before the last word is irrelevant, so
        there's no need to scan it.

        Time:  O(n) worst case (e.g. a string of all spaces except one
               word at the very front), but in practice only scans as
               far back as the last word plus its trailing spaces.
        Space: O(1) -- no intermediate list of words is built.
        """
        i = len(s) - 1

        # Skip trailing spaces.
        while i >= 0 and s[i] == " ":
            i -= 1

        length = 0
        while i >= 0 and s[i] != " ":
            length += 1
            i -= 1

        return length


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ("Hello World", 5),
        ("   fly me   to   the moon  ", 4),
        ("luffy is still joyboy", 6),
        ("a", 1),
        ("   a", 1),
        ("a   ", 1),
        ("day", 3),
        ("   day   ", 3),
        ("a b c", 1),
        ("  hello   world  ", 5),
    ]

    methods = [
        ("lengthOfLastWord (split)", solution.lengthOfLastWord),
        ("lengthOfLastWordTwoPointer (backward scan)", solution.lengthOfLastWordTwoPointer),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (s, expected) in enumerate(test_cases, 1):
            actual = method(s)
            assert actual == expected, (
                f"Test {i} FAILED for {name}: s={s!r}\n"
                f"  expected={expected}, actual={actual}"
            )
            print(f"  Test {i} passed: s={s!r} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()