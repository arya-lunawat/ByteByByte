"""
LeetCode 45 - Jump Game II
https://leetcode.com/problems/jump-game-ii/

You are given a 0-indexed array of integers nums of length n. You are
initially positioned at nums[0]. Each element nums[i] represents the
maximum length of a forward jump from index i. In other words, if you
are at nums[i], you can jump to any nums[i + j] where:
    0 <= j <= nums[i]
    i + j < n

Return the minimum number of jumps to reach nums[n - 1]. The test
cases are generated such that you can always reach nums[n - 1].
"""

from typing import List


class SolutionBruteForce:
    """
    Approach: Bottom-up DP -- min jumps to reach each index.

    dp[i] = minimum number of jumps needed to reach index i from index
    0. dp[0] = 0. For every index i, look at every index j < i that
    could have jumped to i (i.e. j + nums[j] >= i) and take the best
    (minimum) dp[j] + 1 among them.

    This is a correct but quadratic approach: for each index i we scan
    all previous indices j to check if a jump from j can reach i,
    rather than directly computing, from each index, the farthest
    reachable point in one pass (which is what the greedy approach
    does in linear time).

    Time:  O(n^2) -- for each of n indices, scan up to n previous
           indices to find a valid predecessor.
    Space: O(n) for the dp array.
    """

    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [float("inf")] * n
        dp[0] = 0

        for i in range(1, n):
            for j in range(i):
                if j + nums[j] >= i:
                    dp[i] = min(dp[i], dp[j] + 1)

        return dp[n - 1]


class Solution:
    """
    Approach: Greedy, BFS-layer-by-layer (implicit levels).

    Think of this as a breadth-first search over "how far can I get in
    k jumps", without ever building an explicit graph. Track three
    values while scanning left to right:

      - `jumps`: the answer so far (number of jumps used).
      - `current_end`: the farthest index reachable using the jumps
        taken so far -- i.e. the boundary of the current BFS "layer".
      - `farthest`: the farthest index reachable from any position
        visited within the current layer, using ONE more jump.

    As we scan index i from 0 to n - 2, we update
    farthest = max(farthest, i + nums[i]) -- this represents "if I use
    one more jump from somewhere in the current layer, how far could I
    possibly reach?" When i reaches current_end (we've examined every
    index in the current layer and can't extend the current jump count
    any further without committing to another jump), we increment
    jumps and set current_end = farthest, moving to the next layer.

    We stop scanning once current_end >= n - 1, since the last index is
    already guaranteed reachable within the jump count found so far.

    Time:  O(n) -- single pass over the array.
    Space: O(1) -- only a few counters.
    """

    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        jumps = 0
        current_end = 0
        farthest = 0

        for i in range(n - 1):
            farthest = max(farthest, i + nums[i])

            if i == current_end:
                jumps += 1
                current_end = farthest

                if current_end >= n - 1:
                    break

        return jumps


if __name__ == "__main__":
    tests = [
        ([2, 3, 1, 1, 4], 2),
        ([2, 3, 0, 1, 4], 2),
        ([1], 0),
        ([1, 1, 1, 1], 3),
        ([5, 1, 1, 1, 1], 1),
        ([1, 2], 1),
        ([2, 1], 1),
        ([2, 1, 1, 1, 4], 3),
    ]

    for nums, expected in tests:
        r_brute = SolutionBruteForce().jump(nums[:])
        r_opt = Solution().jump(nums[:])
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"jump({nums}) -> brute={r_brute} [{s_brute}], "
            f"optimal={r_opt} [{s_opt}], expected={expected}"
        )