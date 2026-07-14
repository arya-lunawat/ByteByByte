"""
LeetCode 24 - Swap Nodes in Pairs
https://leetcode.com/problems/swap-nodes-in-pairs/

Given a linked list, swap every two adjacent nodes and return its head.
You must solve the problem without modifying the values in the list's
nodes (i.e., only nodes themselves may be changed.)

Example 1:
    Input: head = [1,2,3,4]
    Output: [2,1,4,3]

Example 2:
    Input: head = []
    Output: []

Example 3:
    Input: head = [1]
    Output: [1]

Constraints:
    The number of nodes in the list is in the range [0, 100].
    0 <= Node.val <= 100
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals = []
        node = self
        seen = set()
        while node and id(node) not in seen:
            seen.add(id(node))
            vals.append(str(node.val))
            node = node.next
        return "[" + ",".join(vals) + "]"


class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Iterative pointer-relinking solution using a dummy head.

        A dummy node before `head` lets us treat swapping the first pair
        the same as swapping any other pair, since there's always a
        "previous" node to update.

        For each pair (first, second), we need to:
          1. Point `prev.next` to `second` (so whatever came before now
             points to the new first node of the pair).
          2. Point `first.next` to whatever comes after `second` (so
             `first`, now in the second position, links to the next
             pair).
          3. Point `second.next` to `first` (completing the swap).
          4. Advance `prev` to `first` (now sitting at the end of the
             just-swapped pair) to prepare for the next iteration.

        Only pointers are changed here - no node's `.val` is ever
        modified, satisfying the "don't modify values" requirement.

        Time Complexity:  O(n) - each node is visited a constant number
                           of times
        Space Complexity: O(1)
        """
        dummy = ListNode(0, head)
        prev = dummy

        while prev.next is not None and prev.next.next is not None:
            first = prev.next
            second = first.next

            first.next = second.next
            second.next = first
            prev.next = second

            prev = first

        return dummy.next

    def swapPairsRecursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Alternative solution: recursive.

        If there are at least two nodes, swap the first pair and set the
        new first node's `.next` to the result of recursively swapping
        pairs in the rest of the list. If there are fewer than two nodes
        left (0 or 1), there's nothing to swap - return as-is.

        Time Complexity:  O(n)
        Space Complexity: O(n) - recursion depth grows with the number
                           of pairs (n/2 recursive calls)
        """
        if head is None or head.next is None:
            return head

        first, second = head, head.next
        first.next = self.swapPairsRecursive(second.next)
        second.next = first

        return second


def build_list(values):
    dummy = ListNode()
    node = dummy
    for v in values:
        node.next = ListNode(v)
        node = node.next
    return dummy.next


def to_list(head):
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    return values


def run_tests():
    sol = Solution()
    test_cases = [
        ([1, 2, 3, 4], [2, 1, 4, 3]),
        ([], []),
        ([1], [1]),
        ([1, 2], [2, 1]),
        ([1, 2, 3], [2, 1, 3]),
        ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5, 6], [2, 1, 4, 3, 6, 5]),
    ]

    all_passed = True
    for values, expected in test_cases:
        head1 = build_list(values)
        result_iter = to_list(sol.swapPairs(head1))

        head2 = build_list(values)
        result_rec = to_list(sol.swapPairsRecursive(head2))

        status = "PASS" if result_iter == expected else "FAIL"
        if result_iter != expected or result_rec != expected:
            all_passed = False
        print(f"[{status}] swapPairs({values}) = {result_iter} "
            f"(expected {expected}) | recursive method = {result_rec}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()