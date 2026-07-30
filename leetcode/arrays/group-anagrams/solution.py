"""
49. Group Anagrams
https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together. You can
return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters
exactly once.

Example:
    Input:  strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Constraints:
    1 <= strs.length <= 10^4
    0 <= strs[i].length <= 100
    strs[i] consists of lowercase English letters.
"""

from typing import List
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Approach 1: Sorted-string key.

        Two strings are anagrams of each other exactly when sorting
        their characters produces the same string. So: sort each
        string to get a canonical "signature", and use that signature
        as a hash map key to collect all strings that share it.

        Time:  O(n * m log m) -- n strings, each of length up to m,
               each costs O(m log m) to sort.
        Space: O(n * m) -- storing every string (once) plus its sorted
               key, across all groups.
        """
        groups: dict[str, List[str]] = defaultdict(list)
        for s in strs:
            key = "".join(sorted(s))
            groups[key].append(s)
        return list(groups.values())

    def groupAnagramsCharCount(self, strs: List[str]) -> List[List[str]]:
        """
        Approach 2: Character-count key (avoids sorting entirely).

        Instead of sorting each string, count how many times each of
        the 26 lowercase letters appears, producing a fixed-length
        26-tuple. Two strings are anagrams exactly when their count
        tuples are identical, so that tuple can serve directly as a
        hash map key (tuples are hashable; a plain list wouldn't be).

        This trades the O(m log m) sort cost for an O(m + 26) = O(m)
        pass to build the counts -- asymptotically better for long
        strings, at the cost of a fixed 26-length key even for short
        strings.

        Time:  O(n * m) -- n strings, each of length up to m, each
               costs O(m) to count characters (26 is a constant).
        Space: O(n * m) -- same overall storage as approach 1, plus a
               O(26) = O(1) count array per string during construction.
        """
        groups: dict[tuple, List[str]] = defaultdict(list)
        for s in strs:
            counts = [0] * 26
            for ch in s:
                counts[ord(ch) - ord("a")] += 1
            groups[tuple(counts)].append(s)
        return list(groups.values())


def _normalize(result: List[List[str]]):
    return sorted(tuple(sorted(group)) for group in result)


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        ),
        ([""], [[""]]),
        (["a"], [["a"]]),
        (
            ["act", "pots", "tops", "cat", "stop", "hat"],
            [["hat"], ["act", "cat"], ["stop", "pots", "tops"]],
        ),
        (["", ""], [["", ""]]),
        (["ab", "ba", "abc"], [["ab", "ba"], ["abc"]]),
        (
            ["abc", "bca", "cab", "xyz", "zyx", "def"],
            [["abc", "bca", "cab"], ["xyz", "zyx"], ["def"]],
        ),
        (["qwerty"], [["qwerty"]]),
    ]

    methods = [
        ("groupAnagrams (sorted-string key)", solution.groupAnagrams),
        ("groupAnagramsCharCount (26-count key)", solution.groupAnagramsCharCount),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (strs, expected) in enumerate(test_cases, 1):
            actual = method(strs[:])

            # Every input string must appear exactly once across all groups.
            flattened = sorted(s for group in actual for s in group)
            assert flattened == sorted(strs), (
                f"Test {i} FAILED for {name}: strs={strs}\n"
                f"  lost or duplicated strings, got groups={actual}"
            )

            # Every group must actually be mutual anagrams.
            for group in actual:
                canon = "".join(sorted(group[0]))
                for s in group:
                    assert "".join(sorted(s)) == canon, (
                        f"Test {i} FAILED for {name}: '{s}' is not an anagram "
                        f"of the rest of its group {group}"
                    )

            assert _normalize(actual) == _normalize(expected), (
                f"Test {i} FAILED for {name}: strs={strs}\n"
                f"  expected={expected}\n  actual={actual}"
            )

            print(f"  Test {i} passed: strs={strs} -> {len(actual)} group(s)")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()