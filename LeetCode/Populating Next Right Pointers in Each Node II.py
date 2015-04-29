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
    def connect(self, root):
        if root is None:
            return
        head = None
        node = root
        while head is None:
            head = root.left or root.right
            node = root
            root = root.next
            if root is None:
                break
        leaf = node.next
        while node:
            pointer1 = None
            pointer2 = None
            if node.left and node.right:
                node.left.next = node.right
                pointer1 = node.right
            else:
                pointer1 = node.left or node.right
            if leaf is None:
                break
            if leaf.left is None and leaf.right is None:
                leaf = leaf.next
                continue
            else:
                pointer2 = leaf.left or leaf.right
            pointer1.next = pointer2
            node = leaf
            leaf = leaf.next
        self.connect(head)
        
if __name__ == "__main__":
    sol = Solution()
    root = TreeNode(0)
    root.left = TreeNode(2)
    root.right = TreeNode(4)    
    sol.connect(root)
