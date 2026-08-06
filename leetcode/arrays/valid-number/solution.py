"""
65. Valid Number
https://leetcode.com/problems/valid-number/

A valid number can be split up into these components (in order):
    1. A decimal number or an integer.
    2. (Optional) An 'e' or 'E', followed by an integer.

A decimal number can be split up into these components (in order):
    1. (Optional) A sign character (either '+' or '-').
    2. One of the following formats:
        a. One or more digits, followed by a dot '.'.
        b. One or more digits, followed by a dot '.', followed by one
           or more digits.
        c. A dot '.', followed by one or more digits.

An integer can be split up into these components (in order):
    1. (Optional) A sign character (either '+' or '-').
    2. One or more digits.

For example, all the following are valid numbers:
["2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3",
 "3e+7", "+6e-1", "53.5e93", "-123.456e789"]
while the following are not valid numbers:
["abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53"]

Given a string s, return true if s is a valid number.

Constraints:
    1 <= s.length <= 20
    s consists of only English letters (both uppercase and
    lowercase), digits (0-9), plus '+', minus '-', or dot '.'.
"""

import re


class Solution:
    def isNumber(self, s: str) -> bool:
        """
        Approach 1: A single anchored regular expression.

        The grammar in the problem statement translates directly into
        a regex:
          - integer      := [+-]? \\d+
          - decimal      := [+-]? ( \\d+\\.\\d* | \\.\\d+ )
                             (covers "4.", "-.9", "3.14", etc.)
          - exponent      := [eE] [+-]? \\d+                  (optional)
          - full pattern := (integer | decimal) exponent?

        Anchoring with ^...$ (or using fullmatch) ensures the *entire*
        string must match -- not just some substring of it -- which is
        what rules out inputs like "1a" or "99e2.5".

        Time:  O(n) -- regex matching over a fixed-structure pattern
               is linear in the input length here (no catastrophic
               backtracking risk, since each alternative is anchored
               and non-ambiguous).
        Space: O(1) extra beyond the compiled pattern (which itself is
               a small constant).
        """
        pattern = re.compile(
            r"^[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?$"
        )
        return bool(pattern.match(s))

    def isNumberStateMachine(self, s: str) -> bool:
        """
        Approach 2: Manual deterministic finite automaton (DFA),
        character by character.

        Models the grammar directly as a state machine instead of
        leaning on a regex engine, tracking a handful of booleans as
        each character is consumed left to right:
          - seen_digit:    at least one digit has been seen so far
                            (required somewhere before any exponent).
          - seen_dot:      a '.' has already been consumed (only one
                            allowed, and not after an exponent starts).
          - seen_exponent: an 'e'/'E' has already been consumed (only
                            one allowed).
          - seen_digit_after_exponent: at least one digit has appeared
                            since the exponent marker (an exponent
                            with no digits, like "1e", is invalid).

        A '+'/'-' sign is only legal as the very first character of
        the whole string, or immediately after an 'e'/'E'. A digit is
        always legal. A '.' is legal only if none has been seen yet
        and no exponent has started. An 'e'/'E' is legal only if none
        has been seen yet and at least one digit has already appeared
        before it. Any other character invalidates the string
        immediately.

        At the end, the string is valid only if at least one digit was
        seen overall, and -- if an exponent marker was used -- at
        least one digit appeared after it too.

        This is more verbose than the regex, but makes every rule in
        the problem's grammar an explicit, individually-testable
        condition, and avoids relying on the regex engine's own
        semantics for edge cases.

        Time:  O(n) -- single left-to-right pass.
        Space: O(1) -- a handful of boolean flags.
        """
        seen_digit = False
        seen_dot = False
        seen_exponent = False
        seen_digit_after_exponent = False

        for i, ch in enumerate(s):
            if ch.isdigit():
                seen_digit = True
                if seen_exponent:
                    seen_digit_after_exponent = True
            elif ch in "+-":
                if i > 0 and s[i - 1] not in "eE":
                    return False
            elif ch == ".":
                if seen_dot or seen_exponent:
                    return False
                seen_dot = True
            elif ch in "eE":
                if seen_exponent or not seen_digit:
                    return False
                seen_exponent = True
            else:
                return False

        return seen_digit and (not seen_exponent or seen_digit_after_exponent)


def run_tests() -> None:
    solution = Solution()

    valid_cases = [
        "2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3",
        "3e+7", "+6e-1", "53.5e93", "-123.456e789", "0", "0.0",
        ".5", "5.", "+.8", "-0",
    ]
    invalid_cases = [
        "abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53",
        ".", "+", "-", "e", ".e1", "1e.", "1ee1", "1e+", "1e-",
        "-.", "+.", "3.14.5",
    ]

    methods = [
        ("isNumber (regex)", solution.isNumber),
        ("isNumberStateMachine (manual DFA)", solution.isNumberStateMachine),
    ]

    for name, method in methods:
        print(f"--- {name} ---")
        for i, s in enumerate(valid_cases, 1):
            actual = method(s)
            assert actual is True, (
                f"Valid-case test {i} FAILED for {name}: s={s!r} -> {actual} "
                f"(expected True)"
            )
            print(f"  Valid test {i} passed: s={s!r} -> True")

        for i, s in enumerate(invalid_cases, 1):
            actual = method(s)
            assert actual is False, (
                f"Invalid-case test {i} FAILED for {name}: s={s!r} -> {actual} "
                f"(expected False)"
            )
            print(f"  Invalid test {i} passed: s={s!r} -> False")
        print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()