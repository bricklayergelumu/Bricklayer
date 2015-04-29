# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.next = None

class Solution:
    # @param root, a tree node
    # @return nothing
    def nextnode(self,node):
        while node:
            if node.left is not None:
                return node.left
            if node.right is not None:
                return node.right
            node = node.next
        return None
    def connect(self, root):
        if root is None:
            return
        if root.left and root.right:
            root.left.next = root.right
        if root.left and root.right is None:
            root.left.next = self.nextnode(root.next)
        if root.right:
            
            
            
