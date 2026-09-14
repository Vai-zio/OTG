 #Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        list1 = []
        list2 = []
        list3 = []
        while l1 != None:
            list1.append(l1.val)
            l1 = l1.next
        while l2 != None:
            list2.append(l2.val)
            l2 = l2.next
        i = 0
        f = False
        while i < len(list1):
            a = list1[-1]+list2[-1]
            if i > len(list2):
                if f:
                    f = False
                    if len(str(a)) == 2:
                        a -= 10
                        f = True
                    list3.append(list1[-1]+1)
                    list1.pop(-1)
                    i+1
                else:
                    if len(str(a)) == 2:
                        a -= 10
                        f = True
                    list3.append(list1[-1])
                    list1.pop(-1)
                    i+1
            else:
                if f:
                    f = False
                    if len(str(a)) == 2:
                        a -= 10
                        f = True
                    list3.append(a+1)
                    list2.pop(-1)
                    list1.pop(-1)
                    i+1
                else:
                    if len(str(a)) == 2:
                        a -= 10
                        f = True
                    list3.append(a)
                    list2.pop(-1)
                    list1.pop(-1)
                    i+1
        head = ListNode(list3[0])
        tail = head
        n = 1
        while n < len(list3)-1:
            tail.next = ListNode(list3[n])
            tail = tail.next
            n + 1
        return head