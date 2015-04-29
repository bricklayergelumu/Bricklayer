# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # @param two ListNodes
    # @return the intersected ListNode
    def getLength(self,node):
        length = 0
        while node:
            length+= 1
            node = node.next
        return length
    def Synchronize(self,headA,headB):
        lengthA = self.getLength(headA)
        lengthB = self.getLength(headB)
        longhead = None
        shorthead = None
        if lengthA >= lengthB:
            longhead = headA
            shorthead = headB
        else:
            longhead = headB
            shorthead = headA
        distance = max(lengthA,lengthB) - min(lengthA,lengthB)
        while distance > 0:
            longhead = longhead.next
            distance-= 1
        while shorthead:
            if shorthead is longhead:
                return shorthead
            shorthead = shorthead.next
            longhead = longhead.next
        return None
    
    def getIntersectionNode(self, headA, headB):
        if headA is None or headB is None:
            return None
        return self.Synchronize(headA,headB)
