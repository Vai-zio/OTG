from AddTwoNumbers import ListNode
from AddTwoNumbers import Solution
testcase1 = [2,3,4,1]
testcase2 = [8,9,2,1]
head = ListNode(testcase1[0])
tail = head
n = 1
while n < len(testcase1):
    tail.next = ListNode(testcase1[n])
    tail = tail.next
    n + 1
head = ListNode(testcase2[0])
tail = head
n = 1
while n < len(testcase2):
    tail.next = ListNode(testcase2[n])
    tail = tail.next
    n + 1
a = Solution(testcase1,testcase2)
print(a)