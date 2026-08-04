"""
LeetCode 47 - Permutation Sequence
https://leetcode.com/problems/permutation-sequence/

The set [1, 2, 3, ..., n] contains a total of n! unique permutations.
By listing and labeling all of the permutations in order, we get the
following sequence for n = 3:
    1. "123"   2. "132"   3. "213"
    4. "231"   5. "312"   6. "321"

Given n and k, return the kth permutation sequence (1-indexed).
"""

from typing import List
import math


class SolutionBruteForce:
    """
    Approach: Generate every permutation in lexicographic order, index
    directly into the kth one.

    Uses itertools.permutations, which (for a sorted input) produces
    permutations in lexicographic order -- exactly matching the
    problem's numbering scheme. Simply materialize all n! of them and
    return the (k-1)th (converting from 1-indexed to 0-indexed).

    This is correct and simple, but wastes an enormous amount of work:
    it builds and stores all n! permutations just to throw away all but
    one of them. For n = 9 (the problem's upper bound), that's
    362,880 permutations generated and discarded.

    Time:  O(n! * n) -- generating n! permutations, each O(n) to build.
    Space: O(n! * n) -- storing every permutation before picking one.
    """

    def getPermutation(self, n: int, k: int) -> str:
        from itertools import permutations

        digits = [str(i) for i in range(1, n + 1)]
        all_perms = list(permutations(digits))
        return "".join(all_perms[k - 1])


class Solution:
    """
    Approach: Direct construction using the factorial number system.

    Key insight: among the permutations of n distinct symbols, fixing
    the first symbol groups the remaining (n-1)! permutations together
    contiguously (in lexicographic order, all permutations starting
    with the same first digit are adjacent). So:

      - There are (n-1)! permutations for each choice of first digit.
      - The block index `k // (n-1)!` (using 0-indexed k) tells us
        which available digit (in sorted order) goes first.
      - The remainder `k % (n-1)!` becomes the new "k" for choosing the
        second digit among the remaining n-1 digits, where now there
        are (n-2)! permutations per choice, and so on recursively.

    This is exactly converting (k - 1) into the "factorial number
    system": at each step, divide by the factorial of the remaining
    digit count to get an index into the still-available digits (kept
    in a list, removed via pop() as they're used), then take the
    remainder and continue with one fewer digit.

    Time:  O(n^2) -- n steps, each doing an O(n) list removal
           (`pop(index)` shifts the remaining elements).
    Space: O(n) for the list of available digits and the result.
    """

    def getPermutation(self, n: int, k: int) -> str:
        digits = [str(i) for i in range(1, n + 1)]
        k -= 1  # convert to 0-indexed

        factorial = math.factorial(n - 1)
        result: List[str] = []

        for remaining in range(n, 0, -1):
            index = k // factorial
            result.append(digits.pop(index))
            k %= factorial

            if remaining > 1:
                factorial //= (remaining - 1)

        return "".join(result)


if __name__ == "__main__":
    tests = [
        (3, 3, "213"),
        (4, 9, "2314"),
        (3, 1, "123"),
        (1, 1, "1"),
        (3, 6, "321"),
        (4, 1, "1234"),
        (4, 24, "4321"),
        (5, 1, "12345"),
        (5, 120, "54321"),
    ]

    for n, k, expected in tests:
        r_brute = SolutionBruteForce().getPermutation(n, k)
        r_opt = Solution().getPermutation(n, k)
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"getPermutation(n={n}, k={k}) -> "
            f"brute={r_brute!r} [{s_brute}], optimal={r_opt!r} [{s_opt}], expected={expected!r}"
        )