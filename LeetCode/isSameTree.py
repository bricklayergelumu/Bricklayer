#-*-coding:utf8-*-
# Definition for a  binary tree node
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    # @param p, a tree node
    # @param q, a tree node
    # @return a boolean
    def isSameTree(self, p, q):
        if p == q == None:
            return True
        if not (p and q):
            return False
        if p.val != q.val:
            return False
        left = self.isSameTree(p.left,q.left)
        right = self.isSameTree(p.right,q.right)
        return left and right
        
