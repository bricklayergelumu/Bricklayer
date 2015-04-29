# Definition for a  binary tree node
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
#         self.next = None

class Solution:
    # @param root, a tree node
    # @return nothing
    def connect(self, root):
        node = root
        if root.left is None:
            return
        root.left.next = root.right
        while node.next is not None:
            node.right.next = node.next.left
            node = node.next
            node.left.next = node.right
        connect(root.left)
        
