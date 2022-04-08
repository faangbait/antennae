import array
import bisect
import collections
import sortedcontainers
import pytest
import logging
import datetime
from typing import List
logger = logging.getLogger(__name__)
import cProfile

def profileit(func):
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + ".profile" # Name the data file sensibly
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper


################################################################################

solverFunc = "setme"

leetcode_inputs = [
    ("input", "output"),
    ("input", "output"),
    ("input", "output"),
]

class Solution:
    def __init__(self, test_input, expected):
        super().__init__()
        self.correct = expected
        start_time = datetime.datetime.now()
        self.result = getattr(self, solverFunc)(*test_input)
        end_time = datetime.datetime.now()
        print(f'{self.result: >15}{"": >5}{self.correct: >15}{"": >5}{(end_time - start_time).microseconds: >15}')

    def smallestMissingValueSubtree(self, parents: List[int], nums: List[int]) -> List[int]:
        return False

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
