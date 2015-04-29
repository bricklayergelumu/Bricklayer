# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    # @param root, a tree node
    # @return an integer
    def __init__(self):
        self.max = 0
    def checkmax(self,value,bsum):
        nodesum = 0
        if bsum > 0:
            nodesum = value + bsum
        else:
            nodesum = value
        if nodesum > self.max:
            self.max = nodesum
            print self.max
        return nodesum
    def pathsum(self,node):
        leftsum = 0
        rightsum = 0
        if node.left:
            leftsum = self.pathsum(node.left)
        if node.right:
            rightsum = self.pathsum(node.right)
        nodesum = self.checkmax(node.val,leftsum + rightsum)
        leftsum = self.checkmax(node.val,leftsum) if leftsum > 0 else node.val
        rightsum = self.checkmax(node.val,rightsum) if rightsum > 0 else node.val
        return max(leftsum,rightsum)
        
            
    def maxPathSum(self, root):
        if root is None:
            return 0
        self.max = root.val
        self.pathsum(root)
        return self.max
if __name__ == "__main__":
    sol = Solution()
    root = TreeNode(-2)
    root.left = TreeNode(6)
    left1 = root.left
    left1.left = TreeNode(0)
    left1.right = TreeNode(-6)
    sol.maxPathSum(root)
