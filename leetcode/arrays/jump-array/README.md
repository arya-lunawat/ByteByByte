# 55. Jump Game

[LeetCode Problem](https://leetcode.com/problems/jump-game/)

## Problem

Given an integer array `nums`, starting at index 0, where `nums[i]`
is the maximum jump length from index `i`, return whether the last
index is reachable.

```
Input:  nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Input:  nums = [3,2,1,0,4]
Output: false
Explanation: You always arrive at index 3, whose max jump length is 0.
```

**Constraints**
- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^5`

This is the yes/no sibling of
[Jump Game II (45)](../45-jump-game-ii/): rather than finding the
*minimum number* of jumps, this only asks *whether reaching the end
is possible at all* — which turns out to need even less bookkeeping.

## Approaches

### 1. Forward greedy — farthest reachable index — `canJump()`

Scan left to right, maintaining `farthest`: the furthest index
reachable using any combination of jumps decided so far. At index
`i`:

- If `i > farthest`, index `i` itself is unreachable — meaning the
  scan already stalled before getting here, so the end is unreachable
  too. Return `False` immediately.
- Otherwise, update `farthest = max(farthest, i + nums[i])`. If
  `farthest` has reached or passed the last index, return `True` right
  away — no need to keep scanning.

The key idea: we never need to know *which* sequence of jumps reaches
a given index, only *whether some* sequence does — and "farthest
reachable so far" is exactly the single number needed to answer that
for every index in one pass.

- **Time:** `O(n)` — one left-to-right pass.
- **Space:** `O(1)` — one running variable.

### 2. Backward greedy — shrinking the goal — `canJumpBackwards()`

Start with the last index as the current "goal". Scan right to left:
for index `i`, if `i + nums[i] >= goal`, then `i` can already reach
the goal in one jump, so `i` becomes the new (earlier, easier) goal —
reaching `i` is now just as good as reaching the original goal
directly. By the time the scan finishes, the goal has been pulled all
the way back to index 0 if and only if the last index was originally
reachable from the start.

- **Time:** `O(n)` — one right-to-left pass.
- **Space:** `O(1)` — one running variable (the current goal index).

Same result as approach 1, viewed from the opposite direction — some
people find "shrink the target" more intuitive than "grow the reach".

## Testing

`solution.py` runs both approaches against 10 test cases, including
the problem's own examples, a single-element array, arrays with
interior zeros that block progress, and cases where the last index is
reached exactly on the final possible jump.

```
python3 solution.py
```

All test cases pass for both implementations.