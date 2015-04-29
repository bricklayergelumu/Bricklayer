#-*-coding:utf8-*-
# Definition for a  binary tree node
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    # @param root, a tree node
    # @return nothing, do it in place
    def __init__(self):
        self.endpoint = None
    def flatten(self, root):
        if(root is None):
            return
        self.endpoint = root
        right = root.right
        root.right = root.left
        root.left = None
        self.flatten(root.right)
        self.endpoint.right = right
        self.flatten(self.endpoint.right)
        return
    
        
        
