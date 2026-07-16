"""
LeetCode 30 - Substring with Concatenation of All Words
https://leetcode.com/problems/substring-with-concatenation-of-all-words/

You are given a string s and an array of strings words. All the strings of
words are of the same length. A concatenated string is a string that
exactly contains all the strings of any permutation of words concatenated.

Return an array of the starting indices of all the concatenated
substrings in s. You can return the answer in any order.

Example:
    s = "barfoothefoobarman", words = ["foo", "bar"]
    -> [0, 9]
       "barfoo" (0..5)  = ["bar","foo"]
       "foobar" (9..14) = ["foo","bar"]
"""

from collections import Counter
from typing import List


class SolutionBruteForce:
    """
    Approach: Check every starting index directly.

    For each starting index i, chop the next len(words) * word_len
    characters into word-sized chunks and compare their multiset of
    words against the target Counter built from `words`.

    Time:  O(n * k * L)  where n = len(s), k = len(words), L = word length
           (n possible start points, each doing O(k) slices of length L)
    Space: O(k) for the counters
    """

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words or not words[0]:
            return []

        word_len = len(words[0])
        num_words = len(words)
        total_len = word_len * num_words
        target = Counter(words)

        result = []
        for i in range(len(s) - total_len + 1):
            seen = Counter()
            for j in range(num_words):
                start = i + j * word_len
                word = s[start:start + word_len]
                seen[word] += 1
                if seen[word] > target.get(word, 0):
                    break
            else:
                result.append(i)

        return result


class Solution:
    """
    Approach: Sliding window per starting offset (0 .. word_len - 1).

    Every valid match is made up of consecutive word-sized chunks, so we
    only ever need to look at positions that are a multiple of word_len
    away from one of `word_len` possible starting offsets. For each
    offset we run a classic "at most / exactly k" sliding window over
    the word-sized chunks:

      - Expand the window by one word on the right.
      - If that word isn't in `target` at all, the window can't contain
        anything useful -> reset the window to start right after it.
      - If the word is in `target` but we now have *too many* copies of
        it, shrink from the left (popping words out of `window_count`)
        until the count is back within bounds.
      - Once the window holds exactly `num_words` words, its left edge
        is a valid starting index.

    This way every word-sized chunk of s is visited O(1) times per
    offset, and there are only word_len offsets total.

    Time:  O(n * L)  where n = len(s), L = word length
           (n / L chunks per offset * word_len offsets = n total chunk
           visits, each doing O(L) work to slice/hash the chunk)
    Space: O(k) for the counters, k = number of distinct words
    """

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words or not words[0]:
            return []

        word_len = len(words[0])
        num_words = len(words)
        total_len = word_len * num_words
        n = len(s)

        if n < total_len:
            return []

        target = Counter(words)
        result = []

        for offset in range(word_len):
            left = offset
            count = 0  # number of words currently in the window
            window_count = Counter()

            for right in range(offset, n - word_len + 1, word_len):
                word = s[right:right + word_len]

                if word not in target:
                    # Word not part of the vocabulary at all: window
                    # can't span across it, so restart fresh after it.
                    window_count.clear()
                    count = 0
                    left = right + word_len
                    continue

                window_count[word] += 1
                count += 1

                # Too many copies of `word`: shrink from the left until
                # we're back within the allowed count for it.
                while window_count[word] > target[word]:
                    left_word = s[left:left + word_len]
                    window_count[left_word] -= 1
                    count -= 1
                    left += word_len

                if count == num_words:
                    result.append(left)
                    # Slide the window forward by one word to look for
                    # the next match, mirroring the "exactly k" pattern.
                    left_word = s[left:left + word_len]
                    window_count[left_word] -= 1
                    count -= 1
                    left += word_len

        return result


if __name__ == "__main__":
    tests = [
        ("barfoothefoobarman", ["foo", "bar"], [0, 9]),
        ("wordgoodgoodgoodbestword", ["word", "good", "best", "word"], []),
        ("barfoofoobarthefoobarman", ["bar", "foo", "the"], [6, 9, 12]),
        ("a", ["a"], [0]),
        ("aaaaaaaaaaaaaa", ["aa", "aa"], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ]

    for s, words, expected in tests:
        got_optimal = sorted(Solution().findSubstring(s, words))
        got_brute = sorted(SolutionBruteForce().findSubstring(s, words))
        exp_sorted = sorted(expected)
        status_opt = "PASS" if got_optimal == exp_sorted else "FAIL"
        status_brute = "PASS" if got_brute == exp_sorted else "FAIL"
        print(
            f"findSubstring({s!r}, {words}) -> optimal={got_optimal} [{status_opt}], "
            f"brute={got_brute} [{status_brute}], expected={exp_sorted}"
        )