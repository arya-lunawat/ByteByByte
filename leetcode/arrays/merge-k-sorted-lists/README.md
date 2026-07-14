# 23. Merge k Sorted Lists

LeetCode: https://leetcode.com/problems/merge-k-sorted-lists/
**Difficulty:** Hard

## Problem

You are given an array of `k` linked lists, each sorted in ascending
order. Merge all of them into a single sorted linked list and return it.

### Examples

| lists | Output |
|---|---|
| `[[1,4,5],[1,3,4],[2,6]]` | `[1,1,2,3,4,4,5,6]` |
| `[]` | `[]` |
| `[[]]` | `[]` |

### Constraints

- `k == lists.length`, `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- Each `lists[i]` is sorted ascending
- Sum of all list lengths `<= 10^4`

## Approach

`solution.py` implements two solutions — both generalize the
two-list-merge idea (LeetCode 21) to `k` lists, but via different
strategies.

### 1. `mergeKLists` — min-heap / priority queue (primary)

Instead of comparing just two candidate nodes at a time, keep a min-heap
containing the *current head* of every non-empty list. At each step:

1. Pop the smallest node from the heap — this is guaranteed to be the
   smallest remaining value across *all* lists.
2. Attach it to the result.
3. If that node has a `.next`, push it into the heap as the new
   candidate from its list.

This is the natural k-way extension of the two-pointer merge: a heap of
size `k` efficiently finds the minimum among up to `k` candidates in
O(log k), rather than the O(k) it would take to linearly scan for the
minimum each step.

**Note on implementation:** heap entries are `(val, counter, node)`
tuples rather than just `(val, node)`. Since `ListNode` objects aren't
orderable, if two nodes ever tied on `val`, Python's heap would try to
compare the nodes directly and raise a `TypeError`. The monotonically
increasing `counter` acts as a tie-breaker that's always comparable,
sidestepping the issue.

**Time:** O(N log k) where `N` is the total number of nodes across all
lists — each node is pushed and popped from a heap of size at most `k`.
**Space:** O(k) for the heap; existing nodes are relinked rather than
copied, so no extra O(N) space is needed for the result itself.

### 2. `mergeKListsDivideAndConquer` — pairwise merge rounds (for comparison)

Repeatedly pair up the lists and merge each pair using the standard
two-list merge routine, replacing the pair with their merged result.
Repeat this over the (shrinking) collection of lists until only one
remains — the same divide-and-conquer structure as the merge step of
merge sort, just applied to whole linked lists instead of individual
elements.

**Time:** O(N log k) — there are O(log k) rounds of pairwise merges (the
list count roughly halves each round), and each round does O(N) total
work summed across all its pairs.
**Space:** O(1) extra beyond the input/output structures (not counting
the O(log k) recursion-free iteration here, which uses no extra stack).

## Running

```bash
python3 solution.py
```

Includes a minimal `ListNode` class plus `build_list` / `to_list` helpers
for converting between Python lists of lists and linked lists. Runs a
built-in test suite (covering the problem's own examples, empty input,
a single empty list, a single non-empty list, negative values with
duplicates, and lists that are each a single descending-order element),
comparing both solutions and printing pass/fail for each case.