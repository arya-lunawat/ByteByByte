# 65. Valid Number

[LeetCode Problem](https://leetcode.com/problems/valid-number/)

## Problem

Determine whether a string `s` is a valid number. The grammar,
per the problem statement:

- A valid number is a **decimal number or integer**, optionally
  followed by `'e'`/`'E'` and another **integer** (the exponent).
- A **decimal number** is an optional sign, followed by either
  `digits.digits`, `digits.`, or `.digits`.
- An **integer** is an optional sign followed by one or more digits.

```
Valid:   "2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3",
         "3e+7", "+6e-1", "53.5e93", "-123.456e789"
Invalid: "abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53"
```

**Constraints**
- `1 <= s.length <= 20`
- `s` consists only of English letters, digits, `'+'`, `'-'`, and
  `'.'`.

This is a classic "grammar validation" problem — notorious for the
sheer number of edge cases (`"."`, `"e3"`, `"1e"`, `"-."`, `"1e+"`,
etc.) that are easy to get subtly wrong.

## Approaches

### 1. A single anchored regular expression — `isNumber()`

The grammar translates almost directly into a regex:

```
integer  := [+-]? \d+
decimal  := [+-]? ( \d+\.\d* | \.\d+ )        # covers "4.", "-.9", "3.14"
exponent := [eE] [+-]? \d+                     # optional
pattern  := ^ (decimal | integer) exponent? $
```

Anchoring the whole pattern (`^...$`, matched with `re.match` against
a pattern that only succeeds on a full match) is what rules out inputs
like `"1a"` or `"99e2.5"` — without the anchors, the regex would
happily match just the numeric *prefix* of an otherwise-invalid
string.

- **Time:** `O(n)` — this particular pattern has no ambiguous
  alternation that could cause catastrophic backtracking, so matching
  is linear in the input length.
- **Space:** `O(1)` extra, beyond the small compiled pattern.

Compact, but leans on trusting the regex to correctly encode every
grammar rule.

### 2. Manual deterministic finite automaton — `isNumberStateMachine()`

Walks the string once, character by character, tracking four booleans:

- `seen_digit` — at least one digit has appeared anywhere so far.
- `seen_dot` — a `.` has already been consumed (at most one allowed,
  and never after an exponent starts).
- `seen_exponent` — an `e`/`E` has already been consumed (at most one
  allowed).
- `seen_digit_after_exponent` — at least one digit has appeared since
  the exponent marker (an exponent with no digits, like `"1e"`, is
  invalid).

Rules per character: a sign (`+`/`-`) is legal only as the very first
character or immediately after `e`/`E`; a digit is always legal; a
`.` is legal only if none has been seen yet and no exponent has
started; an `e`/`E` is legal only if none has been seen yet and at
least one digit already appeared before it. Anything else invalidates
the string on the spot. At the end, the string is valid only if a
digit was seen overall, and — if an exponent was used — a digit also
appeared after it.

- **Time:** `O(n)` — a single left-to-right pass.
- **Space:** `O(1)` — a handful of boolean flags.

More verbose than the regex, but makes every grammar rule an explicit
condition rather than delegating to a regex engine, which can be
easier to audit or extend for related "parse this restricted grammar"
problems.

## Testing

`solution.py` runs both approaches against 18 valid and 20 invalid
strings — covering the problem's own examples plus edge cases like a
lone `.`, a lone sign, a lone `e`, an exponent with no digits before
or after it, a double exponent, a double dot, and a doubled sign.

```
python3 solution.py
```

All test cases pass for both implementations.