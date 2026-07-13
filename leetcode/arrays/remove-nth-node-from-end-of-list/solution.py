"""
LeetCode 19 - Remove Nth Node From End of List
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Given the head of a linked list, remove the nth node from the end of the
list and return its head.

Example 1:
    Input: head = [1,2,3,4,5], n = 2
    Output: [1,2,3,5]

Example 2:
    Input: head = [1], n = 1
    Output: []

Example 3:
    Input: head = [1,2], n = 1
    Output: [1]

Constraints:
    The number of nodes in the list is sz.
    1 <= sz <= 30
    0 <= Node.val <= 100
    1 <= n <= sz
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
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        One-pass two-pointer solution.

        Use a dummy node before `head` so removing the head itself (when
        n equals the list length) doesn't need special-casing. Advance a
        "fast" pointer n+1 steps ahead of a "slow" pointer (both starting
        at dummy), then move both forward together until fast falls off
        the end. At that point slow sits exactly one node before the
        target, so slow.next is the node to remove.

        Time Complexity:  O(L) where L is the list length - one full
                           pass, no need to first count the list length
        Space Complexity: O(1)
        """
        dummy = ListNode(0, head)
        fast = slow = dummy

        # Move fast n+1 steps ahead so the gap between fast and slow is
        # exactly n+1 nodes; when fast reaches the end (None), slow will
        # be sitting right before the node to remove.
        for _ in range(n + 1):
            fast = fast.next

        while fast is not None:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next

    def removeNthFromEndTwoPass(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Alternative solution: two passes. First pass counts the total
        number of nodes, then a second pass walks to the node just
        before the one to remove (at position length - n from the
        start) and unlinks it.

        Time Complexity:  O(L) - two separate passes over the list, but
                           still linear overall
        Space Complexity: O(1)
        """
        dummy = ListNode(0, head)

        length = 0
        node = head
        while node is not None:
            length += 1
            node = node.next

        # The node to remove is at 0-indexed position (length - n) from
        # head. We walk to the node just before it, starting from dummy.
        prev = dummy
        for _ in range(length - n):
            prev = prev.next

        prev.next = prev.next.next
        return dummy.next


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
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),
        ([1], 1, []),
        ([1, 2], 1, [1]),
        ([1, 2], 2, [2]),
        ([1, 2, 3], 3, [2, 3]),
        ([1, 2, 3, 4, 5, 6, 7], 7, [2, 3, 4, 5, 6, 7]),
    ]

    all_passed = True
    for values, n, expected in test_cases:
        head1 = build_list(values)
        result1 = to_list(sol.removeNthFromEnd(head1, n))

        head2 = build_list(values)
        result2 = to_list(sol.removeNthFromEndTwoPass(head2, n))

        status = "PASS" if result1 == expected else "FAIL"
        if result1 != expected or result2 != expected:
            all_passed = False
        print(f"[{status}] removeNthFromEnd({values}, n={n}) = {result1} "
              f"(expected {expected}) | two-pass method = {result2}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()