# Two Sum

[Problem link](https://leetcode.com/problems/two-sum/)

**Difficulty:** Easy
**Topic:** Arrays, Hash Map

## Problem

Given an array of integers and a target value, return the indices of the
two numbers that add up to the target. Exactly one valid answer exists,
and the same element can't be used twice.

## Approach 1: Brute Force

Check every possible pair of numbers and see if they sum to the target.
Simple to reason about, but doesn't scale well for large inputs.

- **Time:** O(n²) — nested loop over all pairs
- **Space:** O(1) — no extra storage

## Approach 2: Hash Map (Optimal)

Walk through the array once. For each number, compute its complement
(`target - number`) and check if that complement has already been seen.
If it has, we've found our pair immediately. If not, store the current
number and its index and move on.

This trades a bit of space for a big speed win — we go from checking
every pair to a single pass.

- **Time:** O(n) — one pass through the array
- **Space:** O(n) — hash map can hold up to n entries

## Why the hash map wins

The brute force approach re-checks information it already has access to.
The hash map approach remembers what it's seen, so instead of asking
"does any later number pair with this one?" for every element, it asks
"have I already seen the number that pairs with this one?" — which is a
constant-time lookup instead of a linear scan.

## Notes

- Started with brute force to make sure I understood the problem, then
  optimized to the hash map approach.
- Good first problem to establish the "trade space for time" pattern
  that shows up constantly in array/string problems.
