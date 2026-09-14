import math

def binsearch(k,L):
    if len(L) == 0:
        raise ValueError("Searching an empty sequence")
    left = 0
    right = len(L)
    while left <= right:
        m = left + ((right-left) // 2)
        if L[m] < k:
            left = m + 1
        elif L[m] > k:
            right = m - 1
        else:
            return m
    return None

def sortnums(l):
    i = 0
    n = 1
    while i <= len(l):
        if l[i] < l[i+n]:
            i + 1
        return None
    return None

if __name__ == "__main__":
    sorted_nums = [3,8,10,14,65,68,70,71,89,101,162,189,201,333,909,1801]
    idx = binsearch(8,sorted_nums)
    print("I expected log2(length of array), which would equivalate to 4")
    print(f"log2({len(sorted_nums)}) = {math.log2(len(sorted_nums))}")
    print("The number you were looking for in dx is",idx)
    idx = binsearch(101,sorted_nums)
    print("The number you were looking for in ax is", idx)
    idx = binsearch(7,sorted_nums)
    print(idx)