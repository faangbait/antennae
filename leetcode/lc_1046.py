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

solverFunc = "lastStoneWeight"

leetcode_inputs = [
    ([[2,7,4,1,8,1]], 1),
    ([[1]], 1)
]

class Solution:
    def __init__(self, test_input, expected):
        super().__init__()
        self.correct = expected
        start_time = datetime.datetime.now()
        self.result = getattr(self, solverFunc)(*test_input)
        end_time = datetime.datetime.now()
        print(f'{self.result: >15}{"": >5}{self.correct: >15}{"": >5}{(end_time - start_time).microseconds: >15}')

    def lastStoneWeight(self, stones: List[int]) -> int:
        """You are given an array of integers stones where stones[i] is the weight of the ith stone.
        We are playing a game with the stones. On each turn, we choose the heaviest two stones
        and smash them together. Suppose the heaviest two stones have weights x and y with x <= y.
        
        The result of this smash is:
            If x == y, both stones are destroyed, and
            If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
            At the end of the game, there is at most one stone left.

        Args:
            stones (List[int]): A list of stone weights

        Returns:
            int: The smallest possible weight of the left stone. If there are no stones left, return 0.
        """
        def smash(a, b):
            return abs(a-b)

        while len(stones) > 1:
            stones.sort(reverse=True)
            stones.append(smash(stones.pop(0), stones.pop(0)))
        return stones[0]

################################################################################

if __name__ == '__main__':
    print()
    print(f'{"RESULT": >15}{"": >5}{"EXPECTED": >15}{"": >5}{"TIME": >15}')
    print(f'{"":->55}')
    testcases = []
    for test in leetcode_inputs:
        testcases.append(Solution(test[0],test[1]))
    if all([case.result == case.correct for case in testcases]):
        print("!!! All tests passed !!!".rjust(80))
    print()

@pytest.mark.parametrize("test_input,expected", leetcode_inputs)
def test_example_case(test_input, expected):
    assert Solution(test_input, expected).result == expected
