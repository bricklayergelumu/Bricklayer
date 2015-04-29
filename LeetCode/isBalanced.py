#-*-coding:utf8-*-
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
class Solution(object):
    def __init__(self):
        self.result = True
    def HeightCheck(self,node):
        if node == None:
            return 0
        lh = self.HeightCheck(node.left)
        rh = self.HeightCheck(node.right)
        if abs(lh - rh) > 1:
            self.result = False
        return 1 + max(lh,rh)
    def isBalanced(self,root):
        self.HeightCheck(root)
        return self.result
    
if __name__ == "__main__":
    root = TreeNode(1)
    node1 = TreeNode(2)
    node2 = TreeNode(3)
    root.right = node1
    node1.right = node2
    sol = Solution()
    print sol.isBalanced(root)
        
