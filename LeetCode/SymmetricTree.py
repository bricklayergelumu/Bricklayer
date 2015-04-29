#-*-coding:utf8-*-
# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    # @param root, a tree node
    # @return a boolean        
    def isSymmetric(self, root):
        if root == None:
            return True
        return checkSym(root.left,root.right)
    def checkSym(self,left,right):
        if left == right == None:
            return True
        if not (left and right):
            return False
        if left.val != right.val:
            return False
        return checkSym(left.left,right.right) and checkSym(left.right,right.left)
    
if __name__ == "__main__":
    sol = Solution()
    
    
        
        
        
        
