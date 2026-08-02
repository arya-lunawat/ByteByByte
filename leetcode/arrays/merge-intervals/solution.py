"""
56. Merge Intervals
https://leetcode.com/problems/merge-intervals/

Given an array of intervals where intervals[i] = [starti, endi],
merge all overlapping intervals, and return an array of the
non-overlapping intervals that cover all the intervals in the input.

Example:
    Input:  intervals = [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]
    Explanation: Since intervals [1,3] and [2,6] overlap, merge them
    into [1,6].

    Input:  intervals = [[1,4],[4,5]]
    Output: [[1,5]]
    Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
    1 <= intervals.length <= 10^4
    intervals[i].length == 2
    0 <= starti <= endi <= 10^4
"""

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Approach 1: Sort by start, then sweep and merge.

        Once intervals are sorted by their start value, any interval
        that overlaps a previously merged interval must overlap the
        *most recently merged* one -- there's no way for an
        already-sorted later interval to overlap an earlier one
        without also overlapping everything merged in between. So a
        single left-to-right sweep suffices: keep a `merged` list,
        and for each interval, either extend the last merged interval
        (if it overlaps: current.start <= last.end) or append a new
        entry.

        Time:  O(n log n) -- dominated by the sort; the sweep itself
               is O(n).
        Space: O(n) for the sorted copy and the output (O(log n) to
               O(n) for the sort's own internal stack, depending on
               the sort implementation).
        """
        if not intervals:
            return []

        intervals = sorted(intervals, key=lambda pair: pair[0])
        merged = [intervals[0][:]]

        for start, end in intervals[1:]:
            last = merged[-1]
            if start <= last[1]:
                last[1] = max(last[1], end)
            else:
                merged.append([start, end])

        return merged

    def mergeEventCounting(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Approach 2: Sweep-line event counting.

        Treat every interval [start, end] as two events: a "+1" at
        `start` (an interval begins) and a "-1" right after `end`
        (an interval ends, but end itself is still covered, so the
        closing event is placed at end + 1 to make the sweep treat
        touching intervals like [1,4] and [4,5] as overlapping).
        Sort all events by position. Sweep through them, maintaining
        a running "how many intervals are currently open" counter:
        whenever that counter transitions from 0 to positive, a new
        merged interval begins; whenever it drops back to 0, the
        currently-open merged interval ends there.

        This reframes the problem as a classic sweep-line / difference
        array technique, which generalizes well to related problems
        (like counting maximum overlap, or "meeting rooms").

        Time:  O(n log n) -- dominated by sorting the 2n events.
        Space: O(n) for the events list and the output.
        """
        if not intervals:
            return []

        events = []
        for start, end in intervals:
            events.append((start, 1))
            events.append((end + 1, -1))
        events.sort()

        merged = []
        active = 0
        current_start = None

        for position, delta in events:
            if active == 0 and delta == 1:
                current_start = position
            active += delta
            if active == 0:
                merged.append([current_start, position - 1])

        return merged


def _normalize(intervals: List[List[int]]):
    return sorted(tuple(pair) for pair in intervals)


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 4]], [[1, 4]]),
        ([[1, 4], [2, 3]], [[1, 4]]),
        ([[1, 4], [0, 4]], [[0, 4]]),
        ([[1, 4], [5, 6]], [[1, 4], [5, 6]]),
        (
            [[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]],
            [[1, 10]],
        ),
        ([[0, 0], [1, 1], [2, 2]], [[0, 0], [1, 1], [2, 2]]),
    ]

    methods = [
        ("merge (sort + sweep)", solution.merge),
        ("mergeEventCounting (sweep-line events)", solution.mergeEventCounting),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (intervals, expected) in enumerate(test_cases, 1):
            actual = method([pair[:] for pair in intervals])
            assert _normalize(actual) == _normalize(expected), (
                f"Test {i} FAILED for {name}: intervals={intervals}\n"
                f"  expected={expected}\n  actual={actual}"
            )
            print(f"  Test {i} passed: intervals={intervals} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()