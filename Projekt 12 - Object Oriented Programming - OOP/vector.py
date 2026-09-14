import math

class Vector: 
    # constructor (function but inside a class its called a constructur)
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        z = kwargs.get('z', None)
        if kwargs.get('z') == None:
            self.z = 0
        pass

    # Another method
    def __str__(self):
        s = f"Vec({self.x},{self.y})"
        return s
    
    #Another special method
    def __add__(self,other): 
        if self.z and other.z == 0:
            rx = self.x + other.x
            ry = self.y + other.y
            r = Vector(rx,ry)
            return r
        elif self.z and other.z is not 0: 
            rx = self.x + other.x
            ry = self.y + other.y
            rz = self.z + other.z
            r = Vector(rx,ry,rz)
            return r
        return r  #fix return r // doesn't work  :c
    
    def __sub__(self, other):
        if self.z and other.z == 0:
            rx = self.x - other.x
            ry = self.y - other.y
            r = Vector(rx,ry)
            return r
        elif self.z and other.z > 0 or self.z and other.z < 0: 
            rx = self.x + other.x
            ry = self.y + other.y
            rz = self.z + other.z
            r = Vector(rx,ry,rz)
            return r
        return r
    
    def __mul__(self, other):
        rx = self.x * other.x
        ry = self.y * other.y
        r = Vector(rx,ry)
        return r
  
    def length(self):
        # sqrt(a^2+b^2)
        res = round(float(math.sqrt((self.x)^2+(self.y)^2)),3)
        return res

    def cross(self, other):
        if len(self) == 3 and len(other) == 3:
            rx = self.y * other.z - self.z * other.y
            ry = self.z * other.x - self.x * other.z
            rz = self.x * other.y - self.y * other.x
            res = Vector(rx,ry,rz)
            return res
        elif len(self) == 2 and len(other) == 2:
            res = self.x * other.y - self.y * other.x
            return res
        return res