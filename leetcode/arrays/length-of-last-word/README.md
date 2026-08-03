# 58. Length of Last Word

[LeetCode Problem](https://leetcode.com/problems/length-of-last-word/)

## Problem

Given a string `s` of words and spaces, return the length of the
last word — a word being a maximal run of non-space characters.

```
Input:  s = "Hello World"
Output: 5

Input:  s = "   fly me   to   the moon  "
Output: 4

Input:  s = "luffy is still joyboy"
Output: 6
```

**Constraints**
- `1 <= s.length <= 10^4`
- `s` consists only of English letters and spaces `' '`.
- There will be at least one word in `s`.

The tricky part is entirely in the whitespace handling: leading
spaces, trailing spaces, and runs of multiple spaces between words all
need to be ignored without accidentally treating an empty gap as a
zero-length "word".

## Approaches

### 1. Built-in split — `lengthOfLastWord()`

Python's `str.split()` with no separator argument already collapses
runs of whitespace into a single separator and drops leading/trailing
whitespace entirely — so `"   fly me   to   the moon  ".split()`
naturally becomes `['fly', 'me', 'to', 'the', 'moon']` with no empty
strings anywhere. That means the answer is just the length of the
last element.

- **Time:** `O(n)` — `split()` scans the whole string once.
- **Space:** `O(n)` — `split()` builds a list containing every word.

The simplest solution when the language's standard library already
does the hard part.

### 2. Two-pointer backward scan — `lengthOfLastWordTwoPointer()`

Walk backward from the end of the string, without splitting at all:

1. Skip trailing spaces to find the last non-space character (the end
   of the last word).
2. Keep walking backward while characters are non-space, counting
   them, to find where that word starts.

Stop as soon as a space is hit (or the start of the string is
reached) — anything before the last word is irrelevant and never gets
scanned.

- **Time:** `O(n)` worst case, but in practice only scans as far back
  as the last word plus its trailing spaces, rather than the entire
  string.
- **Space:** `O(1)` — no intermediate list of words is ever built.

This is the version worth knowing for the common follow-up
constraint "solve it without using the built-in split", and it's more
memory-efficient on long strings with a short last word.

## Testing

`solution.py` runs both approaches against 10 test cases, including
the problem's own examples, a single character, leading-only and
trailing-only spaces, multiple spaces between every word, and a
last word of length 1.

```
python3 solution.py
```

All test cases pass for both implementations.