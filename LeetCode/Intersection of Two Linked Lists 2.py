# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # @param two ListNodes
    # @return the intersected ListNode
    def getIntersectionNode(self, headA, headB):
        if headA is None or headB is None:
            return None
        p1 = headA
        p2 = headB
        while p1 is not p2:
            p1 = p1.next
            p2 = p2.next
            if p1 is p2:
                return p1
            if p1 is None:
                p1 = headB
            if p2 is None:
                p2 =headA
        return p1
