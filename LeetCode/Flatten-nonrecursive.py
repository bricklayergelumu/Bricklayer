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
        self.endpoint = root
        while root:
            pre = self.endpoint.left
            while pre.right:
                pre = pre.right
            pre.right = self.endpoint.right
            self.endpoint.right = self.endpoint.left
            self.endpoint.left = None
        self.endpoint = self.endpoint.right
            
