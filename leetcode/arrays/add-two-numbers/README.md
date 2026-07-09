# Add Two Numbers

[Problem link](https://leetcode.com/problems/add-two-numbers/)

**Difficulty:** Medium
**Topic:** Linked List, Math

## Problem

Two non-empty linked lists represent two non-negative integers, with
digits stored in **reverse order** (least significant digit first).
Add the two numbers and return the sum as a linked list in the same
reverse-digit format.

Example: `2 -> 4 -> 3` (342) + `5 -> 6 -> 4` (465) = `7 -> 0 -> 8` (807)

## Approach

Simulate long addition, one digit at a time:

1. Walk both lists simultaneously, one node per step.
2. At each step, add the two digits plus any carry from the previous
   step.
3. The new digit is `total % 10`; the new carry is `total // 10`.
4. Keep going until both lists are exhausted **and** there's no carry
   left (a leftover carry, e.g. `999 + 1`, adds one more digit).
5. Build the result list as we go using a dummy head node, which avoids
   special-casing the first node.

Because digits are already stored least-significant-first, this maps
directly onto how addition works on paper — no need to reverse
anything first.

- **Time:** O(max(n, m)) — one pass through the longer of the two lists
- **Space:** O(max(n, m)) — for the output list itself; O(1) auxiliary
  space beyond that

## Edge cases handled

- Lists of different lengths (`l1` or `l2` runs out first — treat
  missing digits as 0)
- Carry propagating past the end of both lists (e.g. `999 + 1 = 1000`,
  which needs an extra node)

## Notes

- Using a dummy head node is a pattern worth remembering for
  linked-list construction problems — it removes the need to
  special-case "is this the first node I'm creating?"
- `build_list` / `list_to_str` in the solution file are just local test
  helpers, not part of what you'd submit on LeetCode (which gives you
  the `ListNode` class and list already built).