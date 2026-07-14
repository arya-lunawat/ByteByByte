# 24. Swap Nodes in Pairs

LeetCode: https://leetcode.com/problems/swap-nodes-in-pairs/
**Difficulty:** Medium

## Problem

Given a linked list, swap every two adjacent nodes and return the head.
The swap must be done by relinking nodes — **node values cannot be
modified**, only the pointers between nodes.

### Examples

| head | Output |
|---|---|
| `[1,2,3,4]` | `[2,1,4,3]` |
| `[]` | `[]` |
| `[1]` | `[1]` |

### Constraints

- Number of nodes is in `[0, 100]`
- `0 <= Node.val <= 100`

## Approach

`solution.py` implements two solutions. Both work purely by relinking
`.next` pointers — no `.val` is ever touched.

### 1. `swapPairs` — iterative with a dummy head (primary)

A `dummy` node before `head` means swapping the very first pair doesn't
need special-casing — there's always a `prev` node whose `.next` needs
updating.

For each pair `(first, second)`, four pointer updates complete the swap:

1. `first.next = second.next` — `first` (now moving to the *second*
   position) points past the pair to whatever comes next.
2. `second.next = first` — `second` (now the *first* node of the pair)
   points to `first`.
3. `prev.next = second` — whatever came before this pair now points to
   the new front of the pair.
4. `prev = first` — advance `prev` to `first`, which now sits at the end
   of the just-swapped pair, ready for the next iteration.

The loop continues as long as there are at least two more nodes
(`prev.next` and `prev.next.next` both exist); a leftover single node at
the end is left untouched.

**Time:** O(n) — each node is visited a constant number of times.
**Space:** O(1)

### 2. `swapPairsRecursive` — recursive (for comparison)

If fewer than two nodes remain, there's nothing to swap — return as-is
(base case). Otherwise, swap the first two nodes directly (`second`
becomes the new head of this segment, pointing to `first`), and set
`first.next` to the result of recursively swapping pairs in the rest of
the list.

**Time:** O(n)
**Space:** O(n) — recursion depth grows with the number of pairs (`n/2`
nested calls), unlike the O(1)-space iterative version.

## Running

```bash
python3 solution.py
```

Includes a minimal `ListNode` class plus `build_list` / `to_list` helpers
for converting between Python lists and linked lists. Runs a built-in
test suite (covering the problem's own example, empty and single-node
lists, both even and odd list lengths, and a leftover unpaired node at
the end), comparing both solutions and printing pass/fail for each case.