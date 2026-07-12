"""
LeetCode 14 - Longest Common Prefix
https://leetcode.com/problems/longest-common-prefix/

Write a function to find the longest common prefix string amongst an
array of strings.

If there is no common prefix, return an empty string "".

Example 1:
    Input: strs = ["flower","flow","flight"]
    Output: "fl"

Example 2:
    Input: strs = ["dog","racecar","car"]
    Output: ""
    Explanation: There is no common prefix among the input strings.

Constraints:
    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] consists of only lowercase English letters.
"""


class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        """
        Vertical scanning: compare characters column by column across all
        strings, starting from the shortest string as the natural upper
        bound for how long any common prefix can be. This avoids building
        up unnecessary substrings and stops as early as possible.

        Time Complexity:  O(S) where S is the sum of all characters in
                           all strings (worst case we scan every char of
                           the shortest string against every other string)
        Space Complexity: O(1) extra (excluding the output string)
        """
        if not strs:
            return ""

        shortest = min(strs, key=len)

        for i, char in enumerate(shortest):
            for other in strs:
                if other[i] != char:
                    return shortest[:i]

        return shortest

    def longestCommonPrefixSort(self, strs: list[str]) -> str:
        """
        Alternative solution: sort the array lexicographically. Once
        sorted, the common prefix of the *entire* array must equal the
        common prefix of just the first and last strings, since any
        divergence would be reflected in how they compare to strings in
        between.

        Time Complexity:  O(S log n) - O(n log n) string comparisons for
                           the sort (each comparison up to O(S/n) chars),
                           plus O(m) for the final prefix scan
        Space Complexity: O(n log n) or O(S) depending on the sort
                           implementation (Python's sort is not in-place
                           w.r.t. comparisons, but uses O(n) auxiliary
                           space)
        """
        if not strs:
            return ""

        strs_sorted = sorted(strs)
        first, last = strs_sorted[0], strs_sorted[-1]

        i = 0
        while i < len(first) and i < len(last) and first[i] == last[i]:
            i += 1

        return first[:i]


def run_tests():
    sol = Solution()
    test_cases = [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        (["single"], "single"),
        (["", "b"], ""),
        (["abc", "abc", "abc"], "abc"),
        (["ab", "a"], "a"),
        (["reflower", "flow", "flight"], ""),
        (["interspecies", "interstellar", "interstate"], "inters"),
        (["throne"], "throne"),
        (["c", "acc", "ccc"], ""),
    ]

    all_passed = True
    for strs, expected in test_cases:
        result_vertical = sol.longestCommonPrefix(strs)
        result_sort = sol.longestCommonPrefixSort(strs)
        status = "PASS" if result_vertical == expected else "FAIL"
        if result_vertical != expected or result_sort != expected:
            all_passed = False
        print(f"[{status}] longestCommonPrefix({strs}) = {result_vertical!r} "
              f"(expected {expected!r}) | sort method = {result_sort!r}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()