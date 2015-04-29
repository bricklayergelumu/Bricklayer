#-*-coding:utf8-*-
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # @return a ListNode
    def addTwoNumbers(self, l1, l2):
        lh = ListNode(0)
        l3 = lh
        summ = 0
        while l1 or l2:
            if l1 != None:
                summ+= l1.val
                l1 = l1.next
            if l2 != None:
                summ+= l2.val
                l2 = l2.next
            l3.next = ListNode(summ%10)
            l3 = l3.next
            summ/= 10
        if summ == 1:
            l3.next = ListNode(summ)
        return lh.next

if __name__ == "__main__":
    sol = Solution()
    l1 = ListNode(0)
    la = l1
    l2 = ListNode(0)
    lb = l2
    lc = sol.addTwoNumbers(la,lb)
    

    
