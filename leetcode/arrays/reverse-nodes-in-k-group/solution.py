"""
LeetCode 25 - Reverse Nodes in k-Group
https://leetcode.com/problems/reverse-nodes-in-k-group/description/

Given the head of a linked list, reverse the nodes of the list k at a
time, and return the modified list.

k is a positive integer and is less than or equal to the length of the
linked list. If the number of nodes is not a multiple of k then
left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves
may be changed.

Example 1:
    Input: head = [1,2,3,4,5], k = 2
    Output: [2,1,4,3,5]

Example 2:
    Input: head = [1,2,3,4,5], k = 3
    Output: [3,2,1,4,5]

Constraints:
    The number of nodes in the list is n.
    1 <= k <= n <= 5000
    0 <= Node.val <= 1000

Follow-up: Can you solve the problem in O(1) extra memory space?
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
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Iterative in-place reversal, group by group, O(1) extra space.

        For each group of k nodes:
          1. First check whether at least k nodes remain starting here;
             if not, that final partial group is left untouched (per the
             problem's rules).
          2. If a full group exists, reverse just those k nodes in place
             using the standard 3-pointer iterative list-reversal
             technique, then reconnect the group's new head/tail to the
             surrounding list (the node before the group, and whatever
             comes after it).
          3. Move on to the next group, using the *original* first node
             of this group (now at its tail, after reversal) as the
             "previous" anchor for reconnecting the next group.

        A dummy node before `head` avoids special-casing when the very
        first group is reversed (since the new overall head changes).

        Time Complexity:  O(n) - every node is visited a constant number
                           of times across the "check group length" and
                           "reverse group" steps
        Space Complexity: O(1) extra - reverses nodes in place via
                           pointer relinking, no recursion or auxiliary
                           data structures
        """
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # Check if there are at least k nodes left starting from
            # group_prev.next; if not, we're done (leave the remainder
            # as-is).
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if kth is None:
                    return dummy.next

            group_next = kth.next  # node right after this group

            # Reverse the k nodes between group_prev and group_next
            # using standard iterative reversal.
            prev, curr = group_next, group_prev.next
            while curr is not group_next:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt

            # group_prev.next was the old head of this group, which is
            # now its tail after reversal; reconnect it to the group
            # that follows, and hook the new group head up to group_prev.
            new_group_head = prev
            old_group_head = group_prev.next
            group_prev.next = new_group_head
            group_prev = old_group_head

        # (unreachable - loop always returns via the length check above)

    def reverseKGroupRecursive(
        self, head: Optional[ListNode], k: int
    ) -> Optional[ListNode]:
        """
        Alternative solution: recursive. Reverse the first k nodes,
        recursively process the rest of the list starting from the (k+1)th
        node, then attach that processed remainder to the tail of the
        just-reversed group.

        Time Complexity:  O(n)
        Space Complexity: O(n/k) - recursion depth is one call per group
        """
        # First check there are at least k nodes remaining.
        node = head
        for _ in range(k):
            if node is None:
                return head
            node = node.next

        # node now points to the (k+1)th node - the start of the rest
        # of the list, which gets recursively reversed in k-groups.
        new_head = self.reverseKGroupRecursive(node, k)

        # Reverse this group of k nodes, attaching the tail to new_head.
        prev, curr = new_head, head
        for _ in range(k):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        return prev


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
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 5, [5, 4, 3, 2, 1]),
        ([1], 1, [1]),
        ([1, 2, 3, 4, 5, 6], 2, [2, 1, 4, 3, 6, 5]),
        ([1, 2, 3, 4, 5, 6, 7, 8], 3, [3, 2, 1, 6, 5, 4, 7, 8]),
    ]

    all_passed = True
    for values, k, expected in test_cases:
        head1 = build_list(values)
        result_iter = to_list(sol.reverseKGroup(head1, k))

        head2 = build_list(values)
        result_rec = to_list(sol.reverseKGroupRecursive(head2, k))

        status = "PASS" if result_iter == expected else "FAIL"
        if result_iter != expected or result_rec != expected:
            all_passed = False
        print(f"[{status}] reverseKGroup({values}, k={k}) = {result_iter} "
              f"(expected {expected}) | recursive method = {result_rec}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()