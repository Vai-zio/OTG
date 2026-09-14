import math
def rect_collision(x, y, r_p, x2, y2, w2, h2):
    # Find the closest point on the rectangle to the circle's center
    closest_x = max(x2, min(x, x2 + w2))  #circle's x to the rect's x outline
    closest_y = max(y2, min(y, y2 + h2))  #circle's y to the rect's y outline

    # Calculate the distance between the circle's center and this closest point
    distance = math.sqrt((x - closest_x) ** 2 + (y - closest_y) ** 2)

    # If the distance is less than or equal to the circle's radius, there is a collision
    if distance <= r_p:
        return True
    else:
        return False

def circle_collision(x,y,r_p,x3,y3,r3):
    # Calculate the distance between the two circle's center point
    d = math.sqrt((x3 - x)**2 + (y3 - y)**2)
    # If the euclids value is less than the two circle's radius', there is a collision
    if d <= r3+r_p:
        return True
    else:
        return False
