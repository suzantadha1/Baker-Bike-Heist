# collision.py 
import math

blocked_area = []

def add_block(x1, y1, x2, y2):
    #Add a rectangular blocked area
    blocked_area.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

# check the point if it a blocked point
def is_blocked(x, y):
    for (x1, y1, x2, y2) in blocked_area:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False

# fuction that doesn't let the player move if the area is blocked:
def move_collision(t, dx, dy):
    new_x = t.xcor() + dx
    new_y = t.ycor() + dy

    if not is_blocked(new_x, new_y):
        t.goto(new_x,new_y)
