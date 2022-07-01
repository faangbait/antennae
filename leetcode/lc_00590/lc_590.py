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

solverFunc = "postorder"

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children

def build_tree(nums: List):
    stack = [Node(val=nums.pop(0))]
    children=None
    for num in nums:
        if num is None:
            for node in stack:
                if node.children is None:
                    node.children = children
                    children = []
                    break
        else:
            child = Node(val=num)
            stack += [child]
            children += [child]

    for node in stack:
        if node.children is None:
            node.children = children
            children = []
            break
    return stack[0]        

    

leetcode_inputs = [
    ([build_tree([1,None,3,2,4,None,5,6])], [5,6,3,2,4,1]),
    ([build_tree([1,None,2,3,4,5,None,None,6,7,None,8,None,9,10,None,None,11,None,12,None,13,None,None,14])], [2,6,14,11,7,3,12,8,4,13,9,10,5,1])
]


class Solution:
    def __init__(self, test_input, expected):
        super().__init__()
        self.correct = expected
        start_time = datetime.datetime.now()
        self.result = getattr(self, solverFunc)(*test_input)
        end_time = datetime.datetime.now()
        print(f'{self.result}{"": >5}{self.correct}{"": >5}{(end_time - start_time).microseconds: >15}')

    def postorder(self, root: 'Node') -> List[int]:
        """Given the root of an n-ary tree, return the postorder traversal of its nodes' values.
        Nary-Tree input serialization is represented in their level order traversal.
        Each group of children is separated by the null value (See examples)



        Args:
            root (Node): The root node of the tree

        Returns:
            List[int]: A list of Node.val entries representing a postorder traversal
        """
        stack = collections.deque()
        stack.append(root)
        
        ordered = collections.deque()
        while stack:
            cur = stack.pop()
            if hasattr(cur,"val"):
                ordered.append(cur.val)
            if hasattr(cur, "children"):
                if cur.children:
                    for child in getattr(cur, "children", []):
                        stack.append(child)
        ordered.reverse()
        return list(ordered)
   

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
