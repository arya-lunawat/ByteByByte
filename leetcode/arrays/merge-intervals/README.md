# 56. Merge Intervals

[LeetCode Problem](https://leetcode.com/problems/merge-intervals/)

## Problem

Given an array of intervals `intervals[i] = [start_i, end_i]`, merge
all overlapping intervals and return the non-overlapping intervals
that cover everything in the input.

```
Input:  intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: [1,3] and [2,6] overlap, so they merge into [1,6].

Input:  intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: [1,4] and [4,5] are considered overlapping (touching counts).
```

**Constraints**
- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

Note that `[1,4]` and `[4,5]` count as overlapping even though they
only *touch* at `4` rather than truly overlapping — both approaches
below need to handle that edge case correctly.

## Approaches

### 1. Sort by start, then sweep and merge — `merge()`

Sort intervals by their start value. Once sorted, an important
property holds: any interval that overlaps something already merged
must overlap the *most recently merged* interval specifically —
there's no way, once sorted, for a later interval to overlap an
earlier one without also overlapping everything merged in between.
That means a single left-to-right sweep is enough: for each interval,
either extend the last merged interval (when
`current.start <= last.end`) or start a brand-new merged interval.

- **Time:** `O(n log n)` — dominated by the sort; the sweep itself is
  `O(n)`.
- **Space:** `O(n)` for the sorted copy and the output.

This is the standard, most direct solution.

### 2. Sweep-line event counting — `mergeEventCounting()`

Reframe each interval `[start, end]` as two events: a `+1` at
`start` (an interval opens) and a `-1` at `end + 1` (an interval
closes — placed one past `end`, specifically so that touching
intervals like `[1,4]` and `[4,5]` are treated as overlapping rather
than separate). Sort all `2n` events by position, then sweep through
them tracking how many intervals are currently "open": a transition
from `0` open to `1+` open starts a new merged interval, and a drop
back to `0` open closes it.

- **Time:** `O(n log n)` — dominated by sorting the `2n` events.
- **Space:** `O(n)` for the events list and the output.

This is a heavier-weight formulation for this specific problem, but
it's the same sweep-line / difference-array technique that
generalizes directly to related problems — like counting the maximum
number of simultaneously overlapping intervals, or "meeting rooms"
style scheduling questions.

## Testing

`solution.py` runs both approaches against 8 test cases, including
the problem's own examples, a single interval, a fully-nested
interval, touching-but-not-overlapping intervals, a chain of
intervals all absorbed by one large interval, and disjoint
single-point intervals.

```
python3 solution.py
```

All test cases pass for both implementations.