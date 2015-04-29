#-*-coding:utf8-*-
# Definition for singly-linked list with a random pointer.
# class RandomListNode:
#     def __init__(self, x):
#         self.label = x
#         self.next = None
#         self.random = None
class Solution:
    # @param head, a RandomListNode
    # @return a RandomListNode
    def __init__(self):
        self.copyhead = None
    def copyNode(self,node):
        copy = RandomListNode(node.label)
        copy.next = node.next
        copy.random = node.random
        node.next = copy
        return copy.next
    def copyRandomList(self, head):
        if head == None:
            return None
        self.copyhead = head
        while self.copyhead:
            self.copyhead = copyNode(self.copyhead)
        self.copyhead = head.next
        while self.copyhead:
            if self.copyhead.random is not None:
                self.copyhead.random = self.copyhead.random.next
            if self.copyhead.next is not None:
                self.copyhead = self.copyhead.next.next
            else:
                self.copyhead = None
        newList = RandomListNode(0)
        newList.next = head
        ohead = head
        self.copyhead = newList
        while ohead:
            self.copyhead.next = ohead.next
            if self.copyhead.next is not None:
                ohead.next = self.copyhead.next.next
            ohead = ohead.next
            self.copyhead = self.copyhead.next
        return newList
            
            
        
