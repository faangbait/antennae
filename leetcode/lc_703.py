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

leetcode_inputs = [
"""
Input:  ["KthLargest", "add", "add", "add", "add", "add"]
        [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
Output: [null, 4, 5, 5, 8, 8]
"""
]
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.stream = sortedcontainers.SortedList(nums)
        
    def add(self, val: int) -> int:
        self.stream.add(val)
        return self.stream[-self.k]

# @pytest.mark.parametrize("test_input,expected", leetcode_inputs)
def test_example_case():
    obj = KthLargest(3, [4,5,8,2])
    assert obj.add(3) == 4
    assert obj.add(5) == 5
    assert obj.add(10)== 5
    assert obj.add(9) == 8
    assert obj.add(4) == 8
