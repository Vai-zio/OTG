import math, random
class Circle:

    def __init__(self,x,y,r,color=(0,0,0),dx=None,dy=None):
        self.x = x
        self.y = y
        self.r = r
        if color == (0,0,0):
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            self.color = color
        if not dx:
            dx = random.randint(-5,5)
        if not dy:
            dy = random.randint(-5,5)
        self.MoveDirectionX = dx
        self.MoveDirectionY = dy

    def collide(self,other):
        distX = self.x - other.x
        distY = self.y - other.y
        distance = math.sqrt(distX*distX+distY*distY)
        if distance <= (self.r + other.r):
            return True #circles are colliding
        else:
            return False #no collision
        

    def move(self):
        if not self.MoveDirectionX:
            self.MoveDirectionX = int(random.randint(-5,5))
        if not self.MoveDirectionY:
            self.MoveDirectionY = int(random.randint(-5,5))
        self.x += self.MoveDirectionX
        self.y += self.MoveDirectionY
    
    def movedir(self, velocity=None, angle=None):
        """Move circle in a direction given by velocity and angle (in degrees)."""
        # Convert to radians for math functions
        if not velocity:
            velocity = 2
        if not angle:
            angle = random.randint(0,360)
        rad = math.radians(angle)
        self.x += velocity * math.cos(rad)
        self.y -= velocity * math.sin(rad)  # minus because screen y increases downward


    def __str__(self):
        return("self")

class Circle2(Circle):
    pass