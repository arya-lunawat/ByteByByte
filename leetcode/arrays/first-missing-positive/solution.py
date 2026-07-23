"""
LeetCode 41 - First Missing Positive
https://leetcode.com/problems/first-missing-positive/

Given an unsorted integer array nums, return the smallest missing
positive integer.

You must implement an algorithm that runs in O(n) time and uses O(1)
auxiliary space.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Hash set + linear probe from 1 upward.

    Dump every number into a set for O(1) membership checks, then
    starting from 1, keep asking "is k in the set?" and incrementing k
    until we find one that isn't. Since the answer is guaranteed to be
    somewhere in [1, n + 1] (an array of n numbers can "block" at most
    1..n, so n + 1 always works as a fallback), this loop runs at most
    n + 1 times.

    This meets the O(n) *time* requirement, but uses O(n) auxiliary
    space for the set -- violating the problem's O(1) space constraint.
    Included as a simpler, more obviously-correct baseline.

    Time:  O(n) -- one pass to build the set, up to n+1 probes after
    Space: O(n) -- the hash set
    """

    def firstMissingPositive(self, nums: List[int]) -> int:
        num_set = set(nums)
        k = 1
        while k in num_set:
            k += 1
        return k


class Solution:
    """
    Approach: In-place cyclic placement (index = value - 1).

    The key constraint that makes O(1) space possible: the answer must
    be in [1, n + 1] where n = len(nums). So any value outside [1, n]
    is irrelevant to the answer and can be ignored; any value v inside
    [1, n] "belongs" at index v - 1 in a fully correct arrangement
    (nums[0] should hold 1, nums[1] should hold 2, etc.).

    Pass 1 -- place values where they belong: for each index i, if
    nums[i] is a valid, in-range value (1 <= nums[i] <= n) and it's not
    already sitting in its correct home slot, swap it there. Repeat the
    check at the same index after each swap (while loop, not if) since
    the newly swapped-in value might also need to move. Values that are
    <= 0, > n, or already duplicates of what's at their target slot are
    simply left in place (they can never represent the answer).

    Pass 2 -- find the first mismatch: scan left to right; the first
    index i where nums[i] != i + 1 means i + 1 is the smallest missing
    positive. If every slot matches (array is exactly [1, 2, ..., n]),
    the answer is n + 1.

    Each element is swapped into place at most once over the whole
    process (once a value lands in its correct slot, it's never moved
    again), so the total work across both passes is linear despite the
    nested-looking while loop.

    Time:  O(n) -- each index triggers at most one "chain" of swaps,
           and every value is swapped into its final resting place at
           most once across the entire array.
    Space: O(1) -- rearranges nums in place, no extra data structures.
    """

    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)

        for i in range(n):
            while (
                1 <= nums[i] <= n
                and nums[nums[i] - 1] != nums[i]
            ):
                target = nums[i] - 1
                nums[i], nums[target] = nums[target], nums[i]

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1


if __name__ == "__main__":
    tests = [
        ([1, 2, 0], 3),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([], 1),
        ([1, 2, 3], 4),
        ([2, 2], 1),
        ([0, -1, -2], 1),
        ([2, 1], 3),
    ]

    for nums, expected in tests:
        r_brute = SolutionBruteForce().firstMissingPositive(nums[:])
        r_opt = Solution().firstMissingPositive(nums[:])
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"firstMissingPositive({nums}) -> "
            f"brute={r_brute} [{s_brute}], optimal={r_opt} [{s_opt}], expected={expected}"
        )