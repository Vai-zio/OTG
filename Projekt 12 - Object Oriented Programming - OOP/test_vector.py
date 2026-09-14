import vector

a = vector.Vector(3,4)
b = vector.Vector(2,5)
print("a =", a, "|", "b =",b)

print("a.x:", a.x, "|", "a.y:", a.y)
print("b.x:", b.x, "|", "b.y:", b.y)

c = a+b # c = vector.Vector(7,9)
print("c =",c)

d = a-b # c = vector.Vector(1,-1)
print("d =",d)

e = a*b # Skalar produkt
print("e =",e)

print("a.length", a.length(),"|","b.length", b.length())