"""
6. Zigzag Conversion
https://leetcode.com/problems/zigzag-conversion/

The string "PAYPALISHIRING" is written in a zigzag pattern on a given number
of rows like this:

P   A   H   N
A P L S I I G
Y   I   R

And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a
number of rows:

    string convert(string s, int numRows);

Example 1:
    Input: s = "PAYPALISHIRING", numRows = 3
    Output: "PAHNAPLSIIGYIR"

Example 2:
    Input: s = "PAYPALISHIRING", numRows = 4
    Output: "PINALSIGYAHRPI"
    Explanation:
    P     I    N
    A   L S  I G
    Y A   H R
    P     I

Example 3:
    Input: s = "A", numRows = 1
    Output: "A"

Constraints:
    1 <= s.length <= 1000
    s consists of English letters (lower-case and upper-case), ',' and '.'.
    1 <= numRows <= 1000
"""


class Solution:
    def convert(self, s: str, numRows: int) -> str:
        """
        Simulate the zigzag by bucketing characters into rows.

        We walk through the string once, tracking which row we are
        currently "writing" to. The current row moves down from 0 to
        numRows - 1, then bounces back up to 0, repeating this diagonal
        bounce for the whole string. Each character is appended to the
        string buffer for its row. Finally, we concatenate all row buffers
        in order to get the answer.

        Time Complexity:  O(n) - every character is visited and placed into
                           its row exactly once.
        Space Complexity: O(n) - the row buffers together store every
                           character in the string once.
        """
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [""] * numRows
        current_row = 0
        going_down = False

        for char in s:
            rows[current_row] += char

            # Flip direction whenever we hit the top or bottom row.
            if current_row == 0 or current_row == numRows - 1:
                going_down = not going_down

            current_row += 1 if going_down else -1

        return "".join(rows)


if __name__ == "__main__":
    solution = Solution()

    # Example 1
    print(solution.convert("PAYPALISHIRING", 3))  # "PAHNAPLSIIGYIR"

    # Example 2
    print(solution.convert("PAYPALISHIRING", 4))  # "PINALSIGYAHRPI"

    # Example 3
    print(solution.convert("A", 1))                # "A"

    # Additional test cases
    print(solution.convert("AB", 1))                # "AB"
    print(solution.convert("ABC", 5))               # "ABC" (numRows >= length)