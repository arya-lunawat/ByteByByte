"""
LeetCode 21 - Merge Two Sorted Lists
https://leetcode.com/problems/merge-two-sorted-lists/description/

You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list. The list should be made by
splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
    Input: list1 = [1,2,4], list2 = [1,3,4]
    Output: [1,1,2,3,4,4]

Example 2:
    Input: list1 = [], list2 = []
    Output: []

Example 3:
    Input: list1 = [], list2 = [0]
    Output: [0]

Constraints:
    The number of nodes in both lists is in the range [0, 50].
    -100 <= Node.val <= 100
    Both list1 and list2 are sorted in non-decreasing order.
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
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """
        Iterative merge using a dummy head.

        This is the linked-list analog of the merge step in merge sort:
        walk both lists simultaneously, at each step splicing whichever
        current node has the smaller value onto the tail of the result,
        and advancing that list. A dummy node avoids special-casing which
        list contributes the very first node. Once one list is exhausted,
        the remainder of the other list is already sorted, so it can be
        attached directly as-is.

        Time Complexity:  O(m + n) where m, n are the lengths of the two
                           lists - each node is visited exactly once
        Space Complexity: O(1) extra - reuses existing nodes, no new ones
                           allocated (aside from the dummy)
        """
        dummy = ListNode()
        tail = dummy

        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # At most one of list1 / list2 is non-empty here; it's already
        # sorted, so just attach it directly.
        tail.next = list1 if list1 is not None else list2

        return dummy.next

    def mergeTwoListsRecursive(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """
        Alternative solution: recursive merge.

        The smaller head becomes the result's head, and its `.next` is
        whatever the merge of the rest of that list with the other list
        produces - a direct recursive restatement of the same logic as
        the iterative version.

        Time Complexity:  O(m + n)
        Space Complexity: O(m + n) - recursion depth grows with the
                           combined list length (no tail-call optimization
                           in Python)
        """
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        if list1.val <= list2.val:
            list1.next = self.mergeTwoListsRecursive(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoListsRecursive(list1, list2.next)
            return list2


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
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([1, 2, 3], [], [1, 2, 3]),
        ([-10, -5, 0], [-8, -1, 5], [-10, -8, -5, -1, 0, 5]),
        ([1, 1, 1], [1, 1], [1, 1, 1, 1, 1]),
        ([5], [1, 2, 3, 4], [1, 2, 3, 4, 5]),
    ]

    all_passed = True
    for values1, values2, expected in test_cases:
        list1a = build_list(values1)
        list2a = build_list(values2)
        result_iter = to_list(sol.mergeTwoLists(list1a, list2a))

        list1b = build_list(values1)
        list2b = build_list(values2)
        result_rec = to_list(sol.mergeTwoListsRecursive(list1b, list2b))

        status = "PASS" if result_iter == expected else "FAIL"
        if result_iter != expected or result_rec != expected:
            all_passed = False
        print(f"[{status}] mergeTwoLists({values1}, {values2}) = {result_iter} "
            f"(expected {expected}) | recursive method = {result_rec}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()