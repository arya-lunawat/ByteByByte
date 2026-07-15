# 25. Reverse Nodes in k-Group

LeetCode: https://leetcode.com/problems/reverse-nodes-in-k-group/description/
**Difficulty:** Hard

## Problem

Given the head of a linked list, reverse the nodes `k` at a time and
return the modified list. If the number of nodes isn't a multiple of
`k`, the leftover nodes at the end stay in their original order.

Node values can't be changed — only the nodes themselves may be relinked.

### Examples

| head | k | Output |
|---|---|---|
| `[1,2,3,4,5]` | `2` | `[2,1,4,3,5]` |
| `[1,2,3,4,5]` | `3` | `[3,2,1,4,5]` |

### Constraints

- `1 <= k <= n <= 5000`
- `0 <= Node.val <= 1000`

**Follow-up:** Can you solve it with O(1) extra memory?

## Approach

`solution.py` implements two solutions.

### 1. `reverseKGroup` — iterative, O(1) extra space (primary)

Process the list one group of `k` nodes at a time, using a `dummy` node
before `head` so the very first group's reversal (which changes the
overall head of the list) doesn't need special-casing.

For each group, starting from `group_prev` (the node right before the
group):

1. **Check the group is full.** Walk `k` steps ahead from `group_prev`.
   If we run off the end of the list before taking `k` steps, there
   aren't enough nodes left for a full group — leave the remainder as-is
   and return.
2. **Reverse in place.** Use the standard 3-pointer iterative reversal
   (`prev`, `curr`, `nxt`) on just the `k` nodes in this group, stopping
   once `curr` reaches `group_next` (the node right after the group).
3. **Reconnect.** After reversal, `group_prev.next` (the group's
   original first node) is now sitting at the *end* of the reversed
   group, and `prev` holds the group's new head. Point `group_prev.next`
   to the new head, then advance `group_prev` to the old head (now the
   tail) to serve as the anchor for the next group.

Because reversal happens via pointer relinking on the existing nodes —
no new nodes, no recursion, no auxiliary lists — this satisfies the O(1)
extra memory follow-up.

**Time:** O(n) — each node is visited a constant number of times (once
during the "is there a full group?" check, once during reversal).
**Space:** O(1) extra.

### 2. `reverseKGroupRecursive` — recursive (for comparison)

1. Check whether at least `k` nodes remain from `head`; if not, return
   `head` unchanged (base case — leftover partial group).
2. Recursively process everything *after* this group first
   (`reverseKGroupRecursive(node, k)` where `node` is the `k+1`-th node),
   getting back the already-processed head of the rest of the list.
3. Reverse this group's `k` nodes using the standard iterative technique,
   attaching the group's tail (`head`, now at the end after reversal) to
   the recursively-processed remainder.

Conceptually clean since it mirrors "reverse this group, then handle the
rest," but doesn't meet the O(1) space follow-up.

**Time:** O(n)
**Space:** O(n/k) — one recursive call per group.

## Running

```bash
python3 solution.py
```

Includes a minimal `ListNode` class plus `build_list` / `to_list` helpers
for converting between Python lists and linked lists. Runs a built-in
test suite (covering both problem examples, `k=1` as a no-op, `k` equal
to the full list length, a single-node list, and cases with a leftover
partial group at the end), comparing both solutions and printing
pass/fail for each case.