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

class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST(object):
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    """
        Get the number of elements
        Using recursion. Complexity O(logN)
    """

    def size(self):
        return self.recur_size(self.root)

    def recur_size(self, root):
        if root is None:
            return 0
        else:
            return 1 + self.recur_size(root.left) + self.recur_size(root.right)

    """
        Search data in bst
        Using recursion. Complexity O(logN)
    """

    def search(self, val):
        return self.recur_search(self.root, val)

    def recur_search(self, root, val):
        if root is None:
            return False
        if root.val == val:
            return True
        elif val > root.val:     # Go to right root
            return self.recur_search(root.right, val)
        else:                      # Go to left root
            return self.recur_search(root.left, val)

    """
        Insert data in bst
        Using recursion. Complexity O(logN)
    """

    def insert(self, val):
        if self.root:
            return self.recur_insert(self.root, val)
        else:
            self.root = TreeNode(val)
            return True

    def recur_insert(self, root, val):
        if root.val == val:      # The data is already there
            return False
        elif val < root.val:     # Go to left root
            if root.left:          # If left root is a node
                return self.recur_insert(root.left, val)
            else:                  # left root is a None
                root.left = TreeNode(val)
                return True
        else:                      # Go to right root
            if root.right:         # If right root is a node
                return self.recur_insert(root.right, val)
            else:
                root.right = TreeNode(val)
                return True

    """
        Preorder, Postorder, Inorder traversal bst
    """

    def preorder(self, root):
        if root:
            print(str(root.val), end=' ')
            self.preorder(root.left)
            self.preorder(root.right)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(str(root.val), end=' ')
            self.inorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(str(root.val), end=' ')


solverFunc = "lowestCommonAncestor"


def build_tree(nums):
    tree = BST()
    for num in nums:
        if num:
            tree.insert(num)
    return tree.get_root()


leetcode_inputs = [
    ([build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), TreeNode(2), TreeNode(8)], 6),
    ([build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), TreeNode(2), TreeNode(4)], 2),
    ([build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), TreeNode(2), TreeNode(1)], 2),
]


class Solution:
    def __init__(self, test_input, expected):
        super().__init__()
        self.correct = expected
        start_time = datetime.datetime.now()
        self.result = getattr(self, solverFunc)(*test_input).val
        end_time = datetime.datetime.now()
        print(f'{self.result: >15}{"": >5}{self.correct: >15}{"": >5}{(end_time - start_time).microseconds: >15}')

    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST.

        Args:
            root (TreeNode): Root node of the tree
            p (TreeNode): Successor 1, for comparison
            q (TreeNode): Successor 2, for comparison

        Returns:
            TreeNode: The lowest common ancestor
        """
        while root:
            if p.val > root.val < q.val:
                root = root.right
            elif p.val < root.val > q.val:
                root = root.left
            else:
                return root

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
