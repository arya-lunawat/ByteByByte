# 47. Permutation Sequence

**Difficulty:** Hard
**Link:** https://leetcode.com/problems/permutation-sequence/
**Topics:** Math, Recursion

## Problem

The set `[1, 2, 3, ..., n]` contains a total of `n!` unique
permutations.

By listing and labeling all of the permutations in order, we get the
following sequence for `n = 3`:

```
1. "123"   2. "132"   3. "213"
4. "231"   5. "312"   6. "321"
```

Given `n` and `k`, return the `k`th permutation sequence
(**1-indexed**).

### Examples

```
Input: n = 3, k = 3
Output: "213"

Input: n = 4, k = 9
Output: "2314"

Input: n = 3, k = 1
Output: "123"
```

### Constraints

- `1 <= n <= 9`
- `1 <= k <= n!`

## Approach 1: Generate All Permutations, Index Directly

`itertools.permutations` on a sorted input produces permutations in
lexicographic order — exactly matching the problem's numbering scheme.
Materialize all `n!` of them and return the `(k - 1)`th one (converting
from 1-indexed to 0-indexed).

Correct and simple, but wastes an enormous amount of work: it builds
and stores every one of the `n!` permutations just to keep exactly
one. At the problem's upper bound (`n = 9`), that's 362,880
permutations generated and discarded.

- **Time:** `O(n! · n)` — generating `n!` permutations, each `O(n)` to
  build.
- **Space:** `O(n! · n)` — storing every permutation before picking
  one out.

## Approach 2: Direct Construction via the Factorial Number System (Optimal)

**Key insight:** among all permutations of `n` distinct symbols,
fixing the first symbol groups the remaining `(n-1)!` permutations
together *contiguously* in lexicographic order — every permutation
starting with the same first digit sits right next to each other.

That means:

- There are `(n-1)!` permutations for each choice of first digit.
- The block index `k // (n-1)!` (using 0-indexed `k`) tells us which
  available digit — in sorted order — goes first.
- The remainder `k % (n-1)!` becomes the new "k" for choosing the
  *second* digit among the remaining `n-1` digits, where now there are
  `(n-2)!` permutations per choice — and so on, recursively, one digit
  at a time.

This is exactly converting `k - 1` into the **factorial number
system**: at each step, divide by the factorial of the remaining digit
count to get an index into the still-available digits (kept in a
list, removed via `pop(index)` as they're used), take the remainder,
and continue with one fewer digit and one smaller factorial.

- **Time:** `O(n^2)` — `n` steps, each doing an `O(n)` list removal
  (`pop(index)` shifts the remaining elements over).
- **Space:** `O(n)` for the list of available digits and the result.

## Files

- [`solution.py`](./solution.py) — both approaches
  (`SolutionBruteForce` and `Solution`), plus inline test cases
  covering the standard examples, the very first permutation (`k = 1`)
  and very last permutation (`k = n!`) for multiple values of `n`, and
  a single-element case (`n = 1`).

## Complexity Summary

| Approach                                    | Time      | Space   |
|--------------------------------------------------|-----------|---------|
| Generate All, Index Directly                       | O(n! · n) | O(n! · n) |
| Factorial Number System (optimal)                  | O(n^2)    | O(n)    |