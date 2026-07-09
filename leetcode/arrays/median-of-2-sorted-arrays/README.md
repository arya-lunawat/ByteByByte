# Median of Two Sorted Arrays

[Problem link](https://leetcode.com/problems/median-of-two-sorted-arrays/)

**Difficulty:** Hard
**Topic:** Binary Search, Arrays, Divide and Conquer

## Problem

Given two sorted arrays `nums1` (size m) and `nums2` (size n), return
the median of the combined sorted array — in O(log(m+n)) time.

Example: `[1,3]` + `[2]` → combined `[1,2,3]` → median `2`

## Approach 1: Merge

Merge both sorted arrays the same way merge sort's merge step does,
then index into the middle (or average the two middle elements for an
even-length combined array).

This is correct and easy to reason about, but it's O(m+n) — it doesn't
meet the O(log(m+n)) requirement the problem specifically asks for.
Included as a baseline / sanity check for the binary search version.

- **Time:** O(m + n)
- **Space:** O(m + n)

## Approach 2: Binary Search on Partitions (Optimal)

The core idea: instead of merging, binary search for a **partition
point** that splits the combined array into a left half and right half
of (roughly) equal size, such that every element in the left half is
≤ every element in the right half. Once that partition is found, the
median can be read directly off the elements bordering the cut — no
merging required.

Steps:
1. Always binary search on the **smaller** of the two arrays (keeps
   the search space small and guarantees valid partition indices
   exist).
2. For a candidate partition index `i` in the smaller array, the
   corresponding partition index `j` in the other array is fully
   determined: `j = (m + n + 1) // 2 - i`.
3. Check the four border values around the cut. If `nums1`'s left
   border ≤ `nums2`'s right border, and vice versa, the partition is
   correct.
4. If not, adjust the binary search bounds and try again.
5. Once correct: odd total length → median is the max of the two left
   borders. Even total length → average of the max left border and
   min right border.

- **Time:** O(log(min(m, n))) — binary search over the smaller array
- **Space:** O(1)

## Why this is the hard part of "Hard"

The tricky part isn't the binary search itself — it's realizing the
problem can be reframed as "find the correct partition" instead of
"find the middle element(s) directly." The four border-value comparison
is what encodes both "left half is smaller than right half" and
"halves are the right size" in one check.

## Notes

- `+inf` / `-inf` sentinels handle the edge cases where a partition
  index lands at the very start or end of an array cleanly, without
  special-casing them separately.
- Tested against the merge-based version on several cases (including
  one array empty, and differing array lengths) to confirm both
  approaches agree.