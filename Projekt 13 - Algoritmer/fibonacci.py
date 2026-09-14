# Fibonacci 0 1 1 2 3 5 8 13 21 34
#           0 1 2 3 4 5 6  7  8  9

def fibprint(n, level=0): #recursive functions call themselves
    print("  "*level,f"fib({n}) called")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibprint(n-2,level+1) + fibprint(n-1,level+1)

def fib(n, level=0): #recursive functions call themselves
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fib(n-2,level+1) + fib(n-1,level+1)

def fibit(n):
    # fn: 0  1  1  2  3  5  8
    #  n: 0  1  2  3  4  5  6
    #        f2 f1 fn
    fn = 0
    f2 = 0
    f1 = 1
    if n == 1:
        return 1
    for i in range(n-1):
        fn = f1 + f2
        f2 = f1
        f1 = fn
    return fn

if __name__ == "__main__":
    #f5 = fib(5)
    #print(f"Fifth fibonacci number is: {f5}")

    #f20 = fibprint(20)
    #print(f"20th fibonacci number is: {f20}")
    
    print("fibit(5)", fibit(5))