"""
5. Longest Palindromic Substring
https://leetcode.com/problems/longest-palindromic-substring/

Given a string s, return the longest palindromic substring in s.

Example 1:
    Input: s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:
    Input: s = "cbbd"
    Output: "bb"

Constraints:
    1 <= s.length <= 1000
    s consist of only digits and English letters.
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Expand Around Center approach.

        For every index in the string, treat it as the potential center of a
        palindrome and expand outwards in both directions while the
        characters match. Because a palindrome can have either an odd length
        (single character center, e.g. "aba") or an even length (two
        character center, e.g. "abba"), we check both cases for each index.

        Time Complexity:  O(n^2) - n possible centers, each expansion can
                           take up to O(n) time.
        Space Complexity: O(1)  - only a constant amount of extra space is
                           used (aside from the output string).
        """
        if not s or len(s) < 1:
            return ""

        start, end = 0, 0

        def expand_around_center(left: int, right: int) -> int:
            """Expand outward from (left, right) while s is a palindrome.
            Returns the length of the palindrome found."""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1

        for i in range(len(s)):
            len1 = expand_around_center(i, i)      # odd length palindrome
            len2 = expand_around_center(i, i + 1)  # even length palindrome
            max_len = max(len1, len2)

            if max_len > end - start + 1:
                start = i - (max_len - 1) // 2
                end = i + max_len // 2

        return s[start:end + 1]


if __name__ == "__main__":
    solution = Solution()

    # Example 1
    print(solution.longestPalindrome("babad"))  # "bab" (or "aba")

    # Example 2
    print(solution.longestPalindrome("cbbd"))    # "bb"

    # Additional test cases
    print(solution.longestPalindrome("a"))       # "a"
    print(solution.longestPalindrome("ac"))      # "a" or "c"
    print(solution.longestPalindrome(""))        # ""