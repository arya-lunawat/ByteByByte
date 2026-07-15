"""
LeetCode 26 - Remove Duplicates from Sorted Array
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Given an integer array nums sorted in non-decreasing order, remove the
duplicates in-place such that each unique element appears only once.
The relative order of the elements should be kept the same. Then return
the number of unique elements in nums.

Consider the number of unique elements of nums to be k, to get accepted,
you need to do the following things:
    - Change the array nums such that the first k elements of nums
      contain the unique elements in the order they were present in nums
      initially. The remaining elements of nums are not important as is
      the size of nums.
    - Return k.

Example 1:
    Input: nums = [1,1,2]
    Output: 2, nums = [1,2,_]
    Explanation: Your function should return k = 2, with the first two
    elements of nums being 1 and 2 respectively. It does not matter what
    you leave beyond the returned k (hence they are underscores).

Example 2:
    Input: nums = [0,0,1,1,1,2,2,3,3,4]
    Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
    Explanation: Your function should return k = 5, with the first five
    elements of nums being 0, 1, 2, 3, and 4 respectively.

Constraints:
    1 <= nums.length <= 3 * 10^4
    -100 <= nums[i] <= 100
    nums is sorted in non-decreasing order.
"""


class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        """
        In-place two-pointer solution.

        Since the array is sorted, all duplicates of a value are
        guaranteed to be adjacent. Use a "write" pointer marking the end
        of the unique-elements-so-far region, and a "read" pointer that
        scans ahead. Whenever the read pointer finds a value different
        from the last written one, it's a new unique element - write it
        just past the current unique region and advance the write
        pointer.

        Because the array is modified in-place and no extra list is
        built, nums itself ends up with its first k elements holding the
        unique values in original order, matching what the problem
        requires.

        Time Complexity:  O(n) - single pass with two pointers
        Space Complexity: O(1) - in-place, no extra data structures
        """
        if not nums:
            return 0

        write = 1  # nums[0] is always unique by definition (nothing before it)

        for read in range(1, len(nums)):
            if nums[read] != nums[write - 1]:
                nums[write] = nums[read]
                write += 1

        return write

    def removeDuplicatesSet(self, nums: list[int]) -> int:
        """
        Alternative solution: use a set to identify unique values (order
        doesn't matter for a sorted array, since duplicates are already
        adjacent), then overwrite nums in-place. Provided mainly for
        comparison; less idiomatic for this problem since it doesn't
        take advantage of the sortedness as directly, and uses O(n)
        extra space.

        Time Complexity:  O(n)
        Space Complexity: O(n) for the intermediate list of unique values
        """
        if not nums:
            return 0

        unique = []
        for val in nums:
            if not unique or unique[-1] != val:
                unique.append(val)

        for i, val in enumerate(unique):
            nums[i] = val

        return len(unique)


def run_tests():
    sol = Solution()
    test_cases = [
        ([1, 1, 2], 2, [1, 2]),
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4]),
        ([1], 1, [1]),
        ([1, 1, 1, 1], 1, [1]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([-3, -3, -1, 0, 0, 0, 5], 4, [-3, -1, 0, 5]),
    ]

    all_passed = True
    for nums, expected_k, expected_prefix in test_cases:
        nums_a = list(nums)
        k_a = sol.removeDuplicates(nums_a)
        prefix_a = nums_a[:k_a]

        nums_b = list(nums)
        k_b = sol.removeDuplicatesSet(nums_b)
        prefix_b = nums_b[:k_b]

        status = "PASS" if (k_a == expected_k and prefix_a == expected_prefix) else "FAIL"
        if k_a != expected_k or prefix_a != expected_prefix or k_b != expected_k or prefix_b != expected_prefix:
            all_passed = False
        print(f"[{status}] removeDuplicates({nums}) -> k={k_a}, prefix={prefix_a} "
            f"(expected k={expected_k}, prefix={expected_prefix}) "
            f"| set method -> k={k_b}, prefix={prefix_b}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()