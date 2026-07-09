"""
LeetCode 3: Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without
repeating characters.

Example:
  Input:  "abcabcbb"
  Output: 3   ("abc" is the longest substring without repeats)

  Input:  "bbbbb"
  Output: 1   ("b")

  Input:  "pwwkew"
  Output: 3   ("wke")
"""


def length_of_longest_substring_brute_force(s: str) -> int:
    """
    Check every possible substring and see if it has all unique
    characters.

    Time:  O(n^3) - O(n^2) substrings, O(n) to check each for uniqueness
    Space: O(min(n, charset)) - for the set used to check uniqueness
    """
    def has_unique_chars(sub: str) -> bool:
        return len(set(sub)) == len(sub)

    n = len(s)
    longest = 0
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j + 1]
            if has_unique_chars(substring):
                longest = max(longest, len(substring))
    return longest


def length_of_longest_substring_optimal(s: str) -> int:
    """
    Sliding window with a hash map of the last seen index of each
    character.

    Keep a window [left, right] that always contains unique characters.
    As we extend `right`, if we hit a character we've seen before *and*
    its last occurrence is inside the current window, jump `left` to
    just past that occurrence instead of shrinking one step at a time.

    Time:  O(n) - each character is visited at most twice (once by
                  `right`, at most once when `left` jumps past it)
    Space: O(min(n, charset)) - hash map holds at most one entry per
                                 unique character
    """
    last_seen = {}  # char -> most recent index
    left = 0
    longest = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        longest = max(longest, right - left + 1)

    return longest


if __name__ == "__main__":
    tests = ["abcabcbb", "bbbbb", "pwwkew", "", "au"]

    for t in tests:
        bf = length_of_longest_substring_brute_force(t)
        opt = length_of_longest_substring_optimal(t)
        print(f"{t!r:12} brute_force={bf}  optimal={opt}")