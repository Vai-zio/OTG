# The number 1007  = 1.007E3 = 10.07E2 = 100.7E1 = 1.007*10^3
num = 69.101*133.7**2
a = 88

print(num)
print(f"num={num:.3f}") # f-string
print(f"num={num:.2E}") # E is short for engineering
print(f"num={num:.2e}") # E is short for engineering (small e means small e in result)
print(f"num={num:.2n}") # n does something not sure what
print(f"num={num:.2g}") # g does something not sure what (same as n)
print(f"num={a:018b}") # b is for binary