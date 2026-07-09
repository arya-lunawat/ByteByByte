"""
LeetCode 2: Add Two Numbers
https://leetcode.com/problems/add-two-numbers/

You are given two non-empty linked lists representing two non-negative
integers. The digits are stored in reverse order, and each node
contains a single digit. Add the two numbers and return the sum as a
linked list, in the same reverse-digit format.

Example:
  Input:  l1 = 2 -> 4 -> 3   (represents 342)
        l2 = 5 -> 6 -> 4   (represents 465)
  Output: 7 -> 0 -> 8        (represents 807, since 342 + 465 = 807)
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Simulate elementary-school addition, one digit at a time, carrying
    over when a column sums to 10 or more.

    Because both lists store digits in reverse order (least significant
    digit first), we can walk both lists left-to-right and it's
    equivalent to adding the numbers right-to-left, like on paper.

    Time:  O(max(n, m)) - one pass through the longer list
    Space: O(max(n, m)) - for the output list (not counting output storage,
                        auxiliary space is O(1))
    """
    dummy_head = ListNode()
    current = dummy_head
    carry = 0

    while l1 is not None or l2 is not None or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10

        current.next = ListNode(digit)
        current = current.next

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy_head.next


# --- helpers for local testing (not part of the LeetCode submission) ---

def build_list(digits: list[int]) -> Optional[ListNode]:
    """Build a linked list from a list of digits, e.g. [2,4,3] -> 2->4->3."""
    dummy = ListNode()
    current = dummy
    for d in digits:
        current.next = ListNode(d)
        current = current.next
    return dummy.next


def list_to_str(node: Optional[ListNode]) -> str:
    vals = []
    while node:
        vals.append(str(node.val))
        node = node.next
    return " -> ".join(vals)


if __name__ == "__main__":
    l1 = build_list([2, 4, 3])   # 342
    l2 = build_list([5, 6, 4])   # 465

    result = add_two_numbers(l1, l2)
    print("Result:", list_to_str(result))  # 7 -> 0 -> 8  (807)

    # edge case: carry propagates through multiple digits
    l1 = build_list([9, 9, 9])   # 999
    l2 = build_list([1])         # 1
    result = add_two_numbers(l1, l2)
    print("Result:", list_to_str(result))  # 0 -> 0 -> 0 -> 1  (1000)