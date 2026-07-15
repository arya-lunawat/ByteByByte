"""
LeetCode 27 - Remove Element
https://leetcode.com/problems/remove-element/description/

Given an integer array nums and an integer val, remove all occurrences
of val in nums in-place. The order of the elements may be changed. Then
return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val to be
k, to get accepted, you need to do the following things:
    - Change the array nums such that the first k elements of nums
      contain the elements which are not equal to val. The remaining
      elements of nums are not important as is the size of nums.
    - Return k.

Example 1:
    Input: nums = [3,2,2,3], val = 3
    Output: 2, nums = [2,2,_,_]
    Explanation: Your function should return k = 2, with the first two
    elements of nums being 2. It does not matter what you leave beyond
    the returned k (hence they are underscores).

Example 2:
    Input: nums = [0,1,2,2,3,0,4,2], val = 2
    Output: 5, nums = [0,1,4,0,3,_,_,_]
    Explanation: Your function should return k = 5, with the first five
    elements of nums containing 0, 0, 1, 3, and 4. Note that the five
    elements can be returned in any order. It does not matter what you
    leave beyond the returned k.

Constraints:
    0 <= nums.length <= 100
    0 <= nums[i] <= 50
    0 <= val <= 100
"""


class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        """
        In-place two-pointer solution ("slow/fast" pointers).

        A "write" pointer tracks where the next kept (non-val) element
        should go, and a "read" pointer scans through the whole array.
        Whenever the read pointer finds a value that isn't `val`, it's
        copied to the write position and write advances. Elements equal
        to `val` are simply skipped by read without touching write.

        This keeps relative order of the kept elements (though the
        problem doesn't require that), and never does more than one pass.

        Time Complexity:  O(n) - single pass with two pointers
        Space Complexity: O(1) - in-place, no extra data structures
        """
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write] = nums[read]
                write += 1

        return write

    def removeElementSwapWithEnd(self, nums: list[int], val: int) -> int:
        """
        Alternative solution: swap-with-end, optimized for when `val` is
        expected to be rare. Instead of shifting every kept element
        forward (which touches most of the array even if only a few
        elements match `val`), swap a matching element with whatever is
        currently at the end of the "active" region and shrink that
        region - avoiding unnecessary writes to elements that already
        don't need to move.

        Note: this does not preserve the relative order of the
        remaining elements (which the problem explicitly allows).

        Time Complexity:  O(n) - each element is visited at most once;
                           in the best case (few matches) far fewer
                           writes happen than the two-pointer method above
        Space Complexity: O(1)
        """
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n - 1]
                n -= 1
                # Don't advance i - the swapped-in value at position i
                # still needs to be checked.
            else:
                i += 1

        return n


def run_tests():
    sol = Solution()
    test_cases = [
        ([3, 2, 2, 3], 3, 2, {2}),
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5, {0, 1, 3, 4}),
        ([], 1, 0, set()),
        ([1, 1, 1], 1, 0, set()),
        ([1, 2, 3], 4, 3, {1, 2, 3}),
        ([2, 2, 2, 2], 2, 0, set()),
    ]

    all_passed = True
    for nums, val, expected_k, expected_multiset in test_cases:
        nums_a = list(nums)
        k_a = sol.removeElement(nums_a, val)
        kept_a = set(nums_a[:k_a])

        nums_b = list(nums)
        k_b = sol.removeElementSwapWithEnd(nums_b, val)
        kept_b = set(nums_b[:k_b])

        status = "PASS" if (k_a == expected_k and kept_a == expected_multiset) else "FAIL"
        if k_a != expected_k or kept_a != expected_multiset or k_b != expected_k or kept_b != expected_multiset:
            all_passed = False
        print(f"[{status}] removeElement({nums}, val={val}) -> k={k_a}, "
            f"kept={sorted(kept_a)} (expected k={expected_k}, "
            f"kept={sorted(expected_multiset)}) | swap method -> k={k_b}, kept={sorted(kept_b)}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()