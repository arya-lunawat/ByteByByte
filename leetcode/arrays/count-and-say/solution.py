"""
LeetCode 38 - Count and Say
https://leetcode.com/problems/count-and-say/

The count-and-say sequence is a sequence of digit strings defined by
the recursive formula:
    countAndSay(1) = "1"
    countAndSay(n) is the run-length encoding of countAndSay(n - 1).

Run-length encoding (RLE) is a string compression method that works by
replacing consecutive identical characters (repeated 2 or more times in
a row) with the concatenation of the character count and the character.
For example, to compress the string "3322251" we replace "33" with
"23", replace "222" with "32", replace "5" with "15" and replace "1"
with "11". Thus the compressed string becomes "23321511".

Given a positive integer n, return the nth element of the count-and-say
sequence.
"""


class SolutionBruteForce:
    """
    Approach: Build each term via naive string concatenation.

    Start from "1" and, for n - 1 iterations, scan the current string
    character by character. Whenever the character changes (or we hit
    the end), append the run's count and character to the result using
    `result += ...`. Repeat until we've generated term n.

    Python strings are immutable, so each `+=` on a string creates a
    brand-new string and copies over the old contents. Doing this
    repeatedly inside the scan of every term means the *string
    building itself* is O(len(result)^2) per term in the worst case,
    on top of the O(len(previous term)) scan -- unlike the optimal
    version, which defers all concatenation to a single `''.join(...)`
    at the very end of each term.

    Time:  Because each term can be up to ~1.5x longer than the last
           (worst case), and the sequence only goes up to n = 30 (the
           longest term still fits comfortably in memory), this stays
           fast in practice for this problem's constraints -- but the
           repeated string `+=` concatenation is an anti-pattern that
           degrades to O(L^2) per term for a term of length L, versus
           O(L) with list-based building.
    Space: O(L) for the current and next strings, L = length of the
           longest term generated (bounded, since n <= 30).
    """

    def countAndSay(self, n: int) -> str:
        result = "1"

        for _ in range(n - 1):
            next_result = ""
            i = 0
            while i < len(result):
                char = result[i]
                count = 0
                while i < len(result) and result[i] == char:
                    count += 1
                    i += 1
                next_result += str(count) + char  # O(len) copy each time
            result = next_result

        return result


class Solution:
    """
    Approach: Two-pointer run-length encoding with list-based building.

    Same core idea as the brute-force version (repeatedly RLE-encode
    the previous term n - 1 times), but avoids the string-concatenation
    pitfall: instead of repeatedly growing a string with `+=`, collect
    each run's "count + digit" piece into a list and join it once per
    term with `''.join(...)`. List appends are amortized O(1), and a
    single join at the end is O(L) for a term of length L -- no
    repeated copying.

    Time:  O(sum of term lengths) across all n terms. The term lengths
           grow slowly (empirically close to, but bounded well under,
           a small constant ratio each step for reasonable n), so this
           is efficient for the problem's constraint (n <= 30).
    Space: O(L) for the current term and the list used to build the
           next one, L = length of the longest term generated.
    """

    def countAndSay(self, n: int) -> str:
        result = "1"

        for _ in range(n - 1):
            pieces = []
            i = 0
            length = len(result)
            while i < length:
                char = result[i]
                j = i
                while j < length and result[j] == char:
                    j += 1
                pieces.append(str(j - i))
                pieces.append(char)
                i = j
            result = "".join(pieces)

        return result


if __name__ == "__main__":
    tests = [
        (1, "1"),
        (2, "11"),
        (3, "21"),
        (4, "1211"),
        (5, "111221"),
        (6, "312211"),
        (7, "13112221"),
        (8, "1113213211"),
    ]

    for n, expected in tests:
        r_brute = SolutionBruteForce().countAndSay(n)
        r_opt = Solution().countAndSay(n)
        s_brute = "PASS" if r_brute == expected else "FAIL"
        s_opt = "PASS" if r_opt == expected else "FAIL"
        print(
            f"countAndSay({n}) -> brute={r_brute!r} [{s_brute}], "
            f"optimal={r_opt!r} [{s_opt}], expected={expected!r}"
        )