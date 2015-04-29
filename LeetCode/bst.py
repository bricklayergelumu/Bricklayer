#-*-coding:utf8-*-
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution(object):
    def __init__(self):
        self.result = []
    def sortedListToArray(self,head):
        ohead = head
        while ohead:
            self.result.append(ohead.val)
            ohead = ohead.next
    def sortedArrayToBST(self,start,end):
        if start > end:
            return
        mid = (start+end)/2
        root = TreeNode(self.result[mid])
        root.left = self.sortedArrayToBST(start,mid-1)
        root.right = self.sortedArrayToBST(mid+1,end)
        return root
    def sortedListToBST(self,head):
        self.sortedListToArray(head)
        length = len(self.result) - 1
        return self.sortedArrayToBST(0,length)
        
        
        
    
if __name__ == "__main__":
    sol = Solution()
    head = ListNode(0)
    sol.sortedListToBST(head)
