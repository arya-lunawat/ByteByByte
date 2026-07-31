# 53. Maximum Subarray

[LeetCode Problem](https://leetcode.com/problems/maximum-subarray/)

## Problem

Given an integer array `nums`, find the subarray with the largest sum
and return that sum. A subarray is a contiguous, non-empty run of
elements.

```
Input:  nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Input:  nums = [1]
Output: 1

Input:  nums = [5,4,-1,7,8]
Output: 23
```

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

The problem's own follow-up asks for both an `O(n)` solution and a
"more subtle" divide-and-conquer solution — both are implemented here.

## Approaches

### 1. Kadane's algorithm — `maxSubArray()`

Walk the array once, tracking `current_sum`: the best possible sum of
a subarray that ends *exactly* at the current index. At each step
there are only two options for that subarray — extend the previous
best-ending-here subarray by adding the current element, or abandon it
and start fresh at the current element:

```
current_sum = max(nums[i], current_sum + nums[i])
```

Starting fresh wins exactly when the running sum has gone negative,
since adding a negative prefix can only drag the total down. The
answer is the largest `current_sum` seen across the whole pass.

- **Time:** `O(n)` — a single pass over the array.
- **Space:** `O(1)` — two running variables, no extra storage.

This is the standard, optimal solution most people reach for.

### 2. Divide and conquer — `maxSubArrayDivideConquer()`

Split the array in half repeatedly. For any range, the best subarray
sum is the best of three candidates:

1. The best subarray entirely within the left half.
2. The best subarray entirely within the right half.
3. The best subarray that **crosses** the midpoint — found by
   extending as far left as possible from the midpoint (the best
   prefix sum ending at `mid`) and as far right as possible (the best
   suffix sum starting at `mid + 1`), then adding those two pieces
   together.

The base case is a single element, whose best subarray is itself.

- **Time:** `O(n log n)` — `log n` levels of recursion, each doing
  `O(n)` work to find the best crossing subarray at that level.
- **Space:** `O(log n)` recursion stack depth.

Asymptotically worse than Kadane's, but it's the "more subtle"
technique the problem explicitly calls out — and the same
divide-and-conquer "combine across the midpoint" pattern shows up
again in problems like closest-pair-of-points.

## Testing

`solution.py` runs both approaches against 10 test cases, including
the problem's own examples, all-negative arrays, all-zero arrays, a
single element, and an array that straddles both negative and
positive values.

```
python3 solution.py
```

All test cases pass for both implementations.