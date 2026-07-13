# 19. Remove Nth Node From End of List

LeetCode: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
**Difficulty:** Medium

## Problem

Given the head of a linked list, remove the `n`-th node from the **end**
of the list and return the (possibly new) head.

### Examples

| head | n | Output |
|---|---|---|
| `[1,2,3,4,5]` | `2` | `[1,2,3,5]` |
| `[1]` | `1` | `[]` |
| `[1,2]` | `1` | `[1]` |

### Constraints

- The number of nodes is `sz`, with `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

## Approach

`solution.py` implements two solutions, both using a **dummy node**
placed before `head`. This is a standard trick for linked-list removal
problems: it means removing the actual head of the list (e.g. when
`n == sz`) doesn't need a separate special case — there's always a real
node before the one being removed.

### 1. `removeNthFromEnd` — one-pass two-pointer (primary)

The classic "runner" technique:

1. Start both `fast` and `slow` at `dummy`.
2. Advance `fast` by `n + 1` steps. This creates a gap of exactly `n + 1`
   nodes between `fast` and `slow`.
3. Move `fast` and `slow` forward together, one step at a time, until
   `fast` runs off the end of the list (`None`).
4. Because the gap was `n + 1`, `slow` now sits exactly on the node
   *just before* the one to remove — regardless of the list's total
   length, which we never had to count. Unlink with `slow.next =
   slow.next.next`.

This works in a single pass because the fixed gap between the two
pointers means "fast reaching the end" happens at exactly the moment
"slow is one node before the target" — no length lookup needed.

**Time:** O(L) where L is the list length — one full traversal.
**Space:** O(1)

### 2. `removeNthFromEndTwoPass` — count then locate (for comparison)

A more direct two-pass approach:

1. First pass: walk the list once to count its total length `L`.
2. Second pass: the node to remove sits at 0-indexed position `L - n`
   from the head, so walk `L - n` steps from `dummy` to land on the node
   just before it, then unlink.

Simpler to reason about, but requires knowing the list length in advance
(here trivial to compute up front), whereas the two-pointer method
doesn't need it at all.

**Time:** O(L) — two separate linear passes, still linear overall.
**Space:** O(1)

## Running

```bash
python3 solution.py
```

Includes a minimal `ListNode` class plus `build_list` / `to_list` helpers
for converting between Python lists and linked lists in the test suite.
Runs a built-in test suite (covering the problem's own examples, removing
the only node in a single-element list, removing from each end of a
two-element list, and removing the head of a longer list), comparing
both solutions and printing pass/fail for each case.