"""
LeetCode 15 - 3Sum
https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets
[nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and
nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2],[-1,0,1]]
    Explanation:
        nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
        nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
        nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
        The distinct triplets are [-1,0,1] and [-1,-1,2].
        Notice that the order of the output and the order of the triplets
        does not matter.

Example 2:
    Input: nums = [0,1,1]
    Output: []
    Explanation: The only possible triplet does not sum up to 0.

Example 3:
    Input: nums = [0,0,0]
    Output: [[0,0,0]]
    Explanation: The only possible triplet sums up to 0.

Constraints:
    3 <= nums.length <= 3000
    -10^5 <= nums[i] <= 10^5
"""


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """
        Sort + two pointers.

        Sort the array first, then fix one number at a time (the
        smallest of the triplet) and use two pointers on the remaining
        sorted subarray to find pairs that sum to its negation - the
        same idea as the classic "Two Sum II" on a sorted array.

        Sorting also makes duplicate-skipping straightforward: once a
        value has been used as the fixed element, skip over any equal
        values; likewise skip duplicate values while advancing the two
        pointers, so we never emit the same triplet twice.

        Time Complexity:  O(n^2) - O(n log n) sort + O(n) fixed elements
                           each doing an O(n) two-pointer scan
        Space Complexity: O(1) extra (excluding the output and the space
                           used by the sort, O(log n) to O(n) depending
                           on implementation)
        """
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n - 2):
            # Skip duplicate values for the fixed element.
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Since the array is sorted, if the smallest possible sum
            # starting here is already positive, no further i can work.
            if nums[i] > 0:
                break

            left, right = i + 1, n - 1
            target = -nums[i]

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    # Skip duplicates for the two-pointer values.
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return result

    def threeSumHashSet(self, nums: list[int]) -> list[list[int]]:
        """
        Alternative solution: sort the array (for easy duplicate
        skipping), fix one element, then use a hash set to find pairs
        summing to the target within the remaining slice - the classic
        "Two Sum" hash approach nested inside a loop over the fixed
        element.

        Time Complexity:  O(n^2) - O(n) fixed elements each doing an
                           O(n) hash-set scan
        Space Complexity: O(n) for the hash set (plus output space)
        """
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                break

            seen = set()
            j = i + 1
            while j < n:
                complement = -nums[i] - nums[j]
                if complement in seen:
                    triplet = [nums[i], complement, nums[j]]
                    if not result or result[-1] != triplet:
                        result.append(triplet)
                    # Skip duplicates of nums[j] to avoid repeat triplets.
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1
                seen.add(nums[j])
                j += 1

        return result


def _normalize(triplets):
    """Sort each triplet and the overall list for order-independent comparison."""
    return sorted(sorted(t) for t in triplets)


def run_tests():
    sol = Solution()
    test_cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
        ([3, 0, -2, -1, 1, 2], [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]),
        ([1, 2, -2, -1], []),
    ]

    all_passed = True
    for nums, expected in test_cases:
        result_two_ptr = sol.threeSum(list(nums))
        result_hash = sol.threeSumHashSet(list(nums))
        norm_result = _normalize(result_two_ptr)
        norm_expected = _normalize(expected)
        status = "PASS" if norm_result == norm_expected else "FAIL"
        if norm_result != norm_expected or _normalize(result_hash) != norm_expected:
            all_passed = False
        print(f"[{status}] threeSum({nums}) = {result_two_ptr} "
              f"(expected {expected}) | hash-set method = {result_hash}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()