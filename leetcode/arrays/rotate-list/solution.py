"""
61. Rotate List
https://leetcode.com/problems/rotate-list/

Given the head of a linked list, rotate the list to the right by k
places.

Example:
    Input:  head = [1,2,3,4,5], k = 2
    Output: [4,5,1,2,3]

    Input:  head = [0,1,2], k = 4
    Output: [2,0,1]

Constraints:
    The number of nodes in the list is in the range [0, 500].
    -100 <= Node.val <= 100
    0 <= k <= 2 * 10^9
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Approach 1: Close the list into a ring, then break it at the
        right spot.

        First walk the list once to find its length and its tail.
        Rotating by any multiple of the length is a no-op, so reduce
        k to k % length up front -- this also cheaply handles the
        huge k values the constraints allow (up to 2 * 10^9) without
        actually performing that many rotations.

        Then temporarily link tail.next = head, turning the list into
        a cycle. The new head is (length - k) steps ahead of the old
        head around that cycle, and the new tail is the node right
        before it -- walk to the new tail and cut the cycle there
        (new_tail.next = None) to produce the rotated list.

        Time:  O(n) -- two passes: one to find the length, one to
               find the new tail.
        Space: O(1) extra -- only pointers, no new nodes allocated.
        """
        if not head or not head.next or k == 0:
            return head

        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        k %= length
        if k == 0:
            return head

        tail.next = head  # close into a ring

        steps_to_new_tail = length - k
        new_tail = head
        for _ in range(steps_to_new_tail - 1):
            new_tail = new_tail.next

        new_head = new_tail.next
        new_tail.next = None
        return new_head

    def rotateRightArrayRebuild(
        self, head: Optional[ListNode], k: int
    ) -> Optional[ListNode]:
        """
        Approach 2: Flatten to a Python list, rotate that list, rebuild
        the linked list from scratch.

        Conceptually the simplest version: collect every node's value
        into a plain list, compute the effective rotation amount
        (k % length), slice the list into "the last k elements" +
        "everything else" (that's exactly what a right-rotation by k
        looks like), and build a brand new linked list from the
        reordered values.

        This trades the O(1) extra space of approach 1 for code that's
        easier to convince yourself is correct at a glance, at the
        cost of allocating an entirely new set of nodes rather than
        reusing the existing ones.

        Time:  O(n) -- one pass to collect values, one to rebuild.
        Space: O(n) -- the intermediate list of values and the new
               linked list.
        """
        if not head or not head.next or k == 0:
            return head

        values = []
        node = head
        while node:
            values.append(node.val)
            node = node.next

        n = len(values)
        k %= n
        if k == 0:
            return head

        rotated_values = values[-k:] + values[:-k]

        new_head = ListNode(rotated_values[0])
        current = new_head
        for val in rotated_values[1:]:
            current.next = ListNode(val)
            current = current.next

        return new_head


def build_list(values: List[int]) -> Optional[ListNode]:
    head = None
    tail = None
    for v in values:
        node = ListNode(v)
        if head is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head


def list_to_values(head: Optional[ListNode]) -> List[int]:
    values = []
    node = head
    while node:
        values.append(node.val)
        node = node.next
    return values


def run_tests() -> None:
    solution = Solution()

    test_cases = [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([0, 1, 2], 4, [2, 0, 1]),
        ([], 0, []),
        ([], 5, []),
        ([1], 0, [1]),
        ([1], 99, [1]),
        ([1, 2], 1, [2, 1]),
        ([1, 2], 2, [1, 2]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 7, [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], 2_000_000_000, None),  # checked via modulo below
    ]

    methods = [
        ("rotateRight (cycle + break)", solution.rotateRight),
        ("rotateRightArrayRebuild (list rebuild)", solution.rotateRightArrayRebuild),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, (values, k, expected) in enumerate(test_cases, 1):
            head = build_list(values)
            result_head = method(head, k)
            actual = list_to_values(result_head)

            if expected is None:
                n = len(values)
                effective_k = k % n if n else 0
                expected = values[-effective_k:] + values[:-effective_k] if effective_k else values[:]

            assert actual == expected, (
                f"Test {i} FAILED for {name}: values={values}, k={k}\n"
                f"  expected={expected}\n  actual={actual}"
            )
            print(f"  Test {i} passed: values={values}, k={k} -> {actual}")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()