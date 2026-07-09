# Longest Substring Without Repeating Characters

[Problem link](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

**Difficulty:** Medium
**Topic:** Strings, Sliding Window, Hash Map

## Problem

Given a string `s`, find the length of the longest substring without
repeating characters.

Example: `"pwwkew"` → `3` (the substring `"wke"`)

## Approach 1: Brute Force

Generate every possible substring, check whether it has all unique
characters, and track the longest one that qualifies.

- **Time:** O(n³) — O(n²) substrings, O(n) to check each for uniqueness
- **Space:** O(min(n, charset)) — for the uniqueness check

## Approach 2: Sliding Window (Optimal)

Maintain a window `[left, right]` over the string that always contains
only unique characters, and a hash map storing the last index each
character was seen at.

- Expand `right` one character at a time.
- If the current character was already seen **inside the current
  window**, jump `left` to just past its last occurrence — no need to
  shrink the window one step at a time.
- After each step, the window size (`right - left + 1`) is a candidate
  for the longest valid substring.

The key insight: once we know a character's last position, we can skip
directly past it instead of walking `left` forward character by
character, which is what makes this O(n) instead of O(n²).

- **Time:** O(n) — each character is looked at by `right` once, and
  `left` only ever moves forward, never backward
- **Space:** O(min(n, charset)) — hash map holds at most one entry per
  distinct character

## Why the window jump matters

A naive sliding window shrinks `left` one step at a time until the
duplicate is removed, which is still O(n²) in the worst case (e.g. a
string like `"aaaaaa...a"`). Jumping `left` directly to
`last_seen[char] + 1` when a duplicate shows up inside the window is
what gets this down to true O(n).

## Notes

- Empty string and single-repeated-character strings (`""`, `"bbbbb"`)
  are useful edge cases to test — both are covered in the test block.
- This sliding-window-with-last-seen-index pattern generalizes to a lot
  of "longest/shortest substring satisfying X" problems.