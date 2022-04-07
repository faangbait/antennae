import array
import bisect
import collections
import sortedcontainers
import pytest
import logging
import datetime
from typing import List
logger = logging.getLogger(__name__)

################################################################################

solverFunc = "numberOfArrays"

leetcode_inputs = [
    (([-40], -46, 53), 60),
    ([[1, -3, 4], 1, 6], 2),
    ([[3, -4, 5, 1, -2], -4, 5], 4),
    ([[4, -7, 2], 3, 6], 0),
    ([[83702, -5216], -82788, 14602], 13689),
    ([[0], 0, 0], 1),
    ([[0], -100000, 100000], 200001)
]


def minmaximumSubarraySum(arr):
    """Generate the min and max sum of a subarray

    Args:
        arr (list): array to consider

    Returns:
        minSum, maxSum: the lower and upper bounds for the first number of the array
    """
    n = len(arr)
    maxSum = -1e8
    minSum = 1e8
    currmaxSum = 0
    currminSum = 0

    for i in range(0, n):
        currmaxSum = currmaxSum + arr[i]
        currminSum = currminSum + arr[i]

        if(currmaxSum > maxSum):
            maxSum = currmaxSum
        if(currmaxSum < 0):
            currmaxSum = 0
        if(currminSum < minSum):
            minSum = currminSum
        if(currminSum > 0):
            currminSum = 0

    return minSum, maxSum


class Solution:
    def __init__(self, test_input, expected):
        super().__init__()
        self.correct = expected
        start_time = datetime.datetime.now()
        self.result = getattr(self, solverFunc)(*test_input)
        end_time = datetime.datetime.now()
        print(f'{self.result: >15}{"": >5}{self.correct: >15}{"": >5}{(end_time - start_time).microseconds: >15}')

    def numberOfArrays(self, differences: List[int], lower: int, upper: int) -> int:
        """You are given a 0-indexed array of n integers differences, which 
        describes the differences between each pair of consecutive integers 
        of a hidden sequence of length (n + 1).

        For example, given differences = [1, -3, 4], lower = 1, upper = 6, 
        the hidden sequence is a sequence of length 4 whose elements are in 
        between 1 and 6 (inclusive).
        [3, 4, 1, 5] and [4, 5, 2, 6] are possible hidden sequences.
        [5, 6, 3, 7] is not possible since it contains an element greater than 6.
        [1, 2, 3, 4] is not possible since the differences are not correct.

        Args:
            differences (List[int]): More formally, call the hidden sequence 
                hidden, then we have that differences[i] = hidden[i + 1] - hidden[i].
            lower (int): You are further given two integers lower and upper 
                that describe the inclusive range of values [lower, upper] that 
                the hidden sequence can contain.
            upper (int): You are further given two integers lower and upper that 
                describe the inclusive range of values [lower, upper] that the 
                hidden sequence can contain.

        Returns:
            int: Return the number of possible hidden sequences there are. If 
            there are no possible sequences, return 0.
        """

        # should be efficient to solve with max sum of subarray to get the 
        # max bound, and the inverse for the min bound. From there on out, it's
        # just math.

        minSum, maxSum = minmaximumSubarraySum(differences)
        dist1 = (-1*((lower+maxSum)-upper))+1
        dist2 = ((upper+minSum)-lower)+1
        res = min(dist1, dist2)
        return max(res, 0)

################################################################################

if __name__ == '__main__':
    print()
    print(f'{"RESULT": >15}{"": >5}{"EXPECTED": >15}{"": >5}{"TIME": >15}')
    print(f'{"":->55}')
    testcases = []
    for test in leetcode_inputs:
        testcases.append(Solution(test[0], test[1]))
    if all([case.result == case.correct for case in testcases]):
        print("!!! All tests passed !!!".rjust(80))
    print()


@pytest.mark.parametrize("test_input,expected", leetcode_inputs)
def test_example_case(test_input, expected):
    assert Solution(test_input, expected).result == expected
