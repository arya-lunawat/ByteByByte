"""
LeetCode 4: Median of Two Sorted Arrays
https://leetcode.com/problems/median-of-two-sorted-arrays/

Given two sorted arrays nums1 and nums2 of size m and n, return the
median of the two combined sorted arrays.

The overall run time complexity should be O(log(m+n)).

Example:
  nums1 = [1, 3], nums2 = [2]
  Combined sorted: [1, 2, 3] -> median = 2

  nums1 = [1, 2], nums2 = [3, 4]
  Combined sorted: [1, 2, 3, 4] -> median = (2 + 3) / 2 = 2.5
"""

from typing import List


def find_median_merge(nums1: List[int], nums2: List[int]) -> float:
    """
    Merge both arrays (like the merge step of merge sort), then read
    off the median. Simple and correct, but doesn't meet the O(log(m+n))
    requirement the problem asks for.

    Time:  O(m + n) - merge both arrays once
    Space: O(m + n) - for the merged array
    """
    merged = []
    i = j = 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])

    n = len(merged)
    mid = n // 2
    if n % 2 == 1:
        return float(merged[mid])
    return (merged[mid - 1] + merged[mid]) / 2.0


def find_median_binary_search(nums1: List[int], nums2: List[int]) -> float:
    """
    Binary search on the smaller array to find the correct partition
    point between both arrays such that:
      - left half has (m + n + 1) // 2 elements
      - every element in the left half <= every element in the right half

    Once we find that partition, the median comes directly from the
    four border elements around the cut, without ever merging anything.

    Time:  O(log(min(m, n))) - binary search over the smaller array
    Space: O(1)
    """
    # Always binary search on the smaller array for efficiency.
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total_left = (m + n + 1) // 2  # size of the combined left half

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2       # partition index in nums1
        j = total_left - i       # partition index in nums2

        # Border values around the cut (use +/- infinity for out-of-range)
        left1 = nums1[i - 1] if i > 0 else float("-inf")
        right1 = nums1[i] if i < m else float("inf")
        left2 = nums2[j - 1] if j > 0 else float("-inf")
        right2 = nums2[j] if j < n else float("inf")

        if left1 <= right2 and left2 <= right1:
            # Correct partition found.
            if (m + n) % 2 == 1:
                return float(max(left1, left2))
            return (max(left1, left2) + min(right1, right2)) / 2.0
        elif left1 > right2:
            # i is too far right, move it left.
            hi = i - 1
        else:
            # i is too far left, move it right.
            lo = i + 1

    raise ValueError("Input arrays are not sorted / invalid input")


if __name__ == "__main__":
    cases = [
        ([1, 3], [2]),
        ([1, 2], [3, 4]),
        ([], [1]),
        ([2], []),
        ([1, 3], [2, 7, 8, 9]),
    ]

    for a, b in cases:
        merge_result = find_median_merge(a, b)
        bs_result = find_median_binary_search(a, b)
        print(f"{a} + {b}  ->  merge={merge_result}  binary_search={bs_result}")