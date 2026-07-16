"""
LeetCode 31 - Next Permutation
https://leetcode.com/problems/next-permutation/

A permutation of an array of integers is an arrangement of its members
into a sequence or linear order.

Given an array of integers `nums`, find the next permutation of `nums`
-- the next lexicographically greater arrangement of its numbers.

If no such arrangement exists (nums is in fully descending order), it
must be rearranged into the lowest possible order (ascending).

The replacement must be done IN PLACE, using only constant extra memory.
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Generate every permutation, sort them, find the current
    one, and return the one right after it (wrapping around to the
    smallest if we're already at the largest).

    This blatantly ignores the "constant extra memory" requirement and
    is only here for comparison -- it materializes O(n!) permutations.

    Time:  O(n! * n log n)  -- generate n! permutations (O(n) each to
           build) and sort them (O(n! log(n!)) comparisons, each O(n))
    Space: O(n! * n)  -- storing every permutation
    """

    def nextPermutation(self, nums: List[int]) -> None:
        from itertools import permutations

        all_perms = sorted(set(permutations(nums)))
        current = tuple(nums)
        idx = all_perms.index(current)
        next_perm = all_perms[(idx + 1) % len(all_perms)]
        nums[:] = list(next_perm)


class Solution:
    """
    Approach: Single-pass, in-place "pivot, swap, reverse".

    The key insight: to get the *next* permutation, we want to make the
    smallest possible increase to the number represented by `nums`,
    changing digits as far to the right (least significant) as we can.

    1. Scan from the right to find the first index `i` where
       nums[i] < nums[i + 1] (the first place, from the right, where
       the sequence stops being non-increasing). This is the "pivot" --
       everything after it is currently the largest possible arrangement
       (strictly non-increasing suffix), so nothing can be improved
       there without changing nums[i] itself.
    2. If no such `i` exists, the whole array is non-increasing -- it's
       already the last permutation, so reverse it entirely to wrap
       around to the smallest (ascending) permutation.
    3. Otherwise, scan from the right again to find the smallest value
       in the suffix that is still greater than nums[i] (the suffix is
       sorted in non-increasing order, so this is the rightmost value
       greater than nums[i] -- swapping with the *rightmost* such value,
       rather than the first one found, correctly handles duplicates).
       Swap it with nums[i].
    4. Reverse everything after index `i` so the suffix becomes ascending
       (the smallest possible arrangement for that suffix), which
       guarantees we made the minimal possible increase.

    Time:  O(n) -- three linear scans over nums in the worst case
    Space: O(1) -- everything done in place
    """

    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)

        # Step 1: find the pivot -- rightmost index where nums[i] < nums[i+1]
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        if i >= 0:
            # Step 3: find rightmost value in suffix greater than nums[i]
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]

        # Step 2 / Step 4: reverse the suffix after the pivot
        # (if i == -1, this reverses the whole array -> smallest permutation)
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


if __name__ == "__main__":
    tests = [
        ([1, 2, 3], [1, 3, 2]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 1, 5], [1, 5, 1]),
        ([1], [1]),
        ([1, 3, 2], [2, 1, 3]),
        ([2, 3, 1], [3, 1, 2]),
        ([1, 5, 1], [5, 1, 1]),
        ([2, 2, 0, 1], [2, 2, 1, 0]),
    ]

    for nums, expected in tests:
        a = nums[:]
        Solution().nextPermutation(a)
        status_opt = "PASS" if a == expected else "FAIL"

        b = nums[:]
        SolutionBruteForce().nextPermutation(b)
        status_brute = "PASS" if b == expected else "FAIL"

        print(
            f"nextPermutation({nums}) -> optimal={a} [{status_opt}], "
            f"brute={b} [{status_brute}], expected={expected}"
        )