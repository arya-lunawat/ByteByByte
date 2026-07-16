# 30. Substring with Concatenation of All Words

**Difficulty:** Hard
**Link:** https://leetcode.com/problems/substring-with-concatenation-of-all-words/
**Topics:** Hash Table, String, Sliding Window

## Problem

You are given a string `s` and an array of strings `words`. All the
strings in `words` are of the **same length**. A *concatenated string*
is a string that exactly contains all the strings of any permutation of
`words` concatenated together (no characters in between, each word used
exactly once — even if a word repeats in `words`, it must repeat that
many times in the match).

Return an array of the starting indices of all concatenated substrings
in `s`. You can return the answer in any order.

### Examples

```
Input: s = "barfoothefoobarman", words = ["foo", "bar"]
Output: [0, 9]
Explanation:
  Substring starting at 0 is "barfoo" -> ["bar","foo"]
  Substring starting at 9 is "foobar" -> ["foo","bar"]

Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
Output: []

Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
Output: [6, 9, 12]
```

### Constraints

- `1 <= s.length <= 10^4`
- `1 <= words.length <= 5000`
- `1 <= words[i].length <= 30`
- `s` and `words[i]` consist of lowercase English letters.

## Approach 1: Brute Force (Check Every Start Index)

For every starting index `i` in `s`, slice out `len(words)` word-sized
chunks and compare their multiset against a `Counter` of `words`. Bail
out early the moment a chunk isn't part of the vocabulary or shows up
too many times.

- **Time:** `O(n * k * L)` — `n` = `len(s)`, `k` = `len(words)`,
  `L` = word length (one `O(k)` scan per start index, each doing an
  `O(L)` slice/hash).
- **Space:** `O(k)` for the counters.

This is simple to reason about but re-does a lot of redundant work,
since adjacent starting indices overlap heavily.

## Approach 2: Sliding Window per Offset (Optimal)

Every valid match is built from consecutive, non-overlapping word-sized
chunks. That means a match can only start at one of `word_len` possible
*offsets* (`0, 1, ..., word_len - 1`) relative to the string. For each
offset, run a single left-to-right sliding window over the word-sized
chunks (an "exactly k occurrences" pattern):

- **Expand:** move the right edge forward by one word.
  - If that word isn't in the target vocabulary at all, the window
    can't possibly stretch across it — clear the window and restart
    right after it.
  - Otherwise add it to the window's word-count.
- **Shrink:** if the window now has *too many* copies of that word,
  pop words off the left edge until the count is valid again.
- **Match:** once the window holds exactly `len(words)` words, its left
  edge is a valid starting index — record it, then slide the window
  forward by one word to keep searching.

Because each offset only touches word-sized chunks and every chunk is
added/removed from the window a constant number of times, this visits
each character of `s` a constant number of times overall.

- **Time:** `O(n * L)` — `n` = `len(s)`, `L` = word length (`word_len`
  offsets, each doing `~n / word_len` chunk visits of `O(L)` work).
- **Space:** `O(k)` for the target/window counters, `k` = number of
  distinct words.

## Files

- [`solution.py`](./solution.py) — both approaches (`SolutionBruteForce`
  and `Solution`), plus inline test cases covering the standard
  examples, a single-word edge case, and a repeated-word/overlapping
  match case.

## Complexity Summary

| Approach                     | Time        | Space |
|-------------------------------|-------------|-------|
| Brute Force (check every start) | O(n · k · L) | O(k) |
| Sliding Window per Offset       | O(n · L)     | O(k) |

*(n = len(s), k = len(words), L = word length)*