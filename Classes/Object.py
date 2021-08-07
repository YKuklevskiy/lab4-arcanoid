import sys
from tkinter import Canvas


# returns 1 if x is positive, -1 if negative, and 0 if zero
def sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


# base class for all game objects
class Object:
    def __init__(self, x, y, instance=None):
        self.x = x
        self.y = y
        self.instance = instance  # canvas instance of object

    name = ''
    size_x = 0
    size_y = 0
    speed = 0

    # creates instance on canvas
    def create_object(self, canvas: Canvas):
        if self.instance is None:
            height = int(canvas['height'])
            self.instance = canvas.create_rectangle([self.x * 8,
                                                     height - self.y * 8,
                                                     (self.x + self.size_x) * 8,
                                                     height - (self.y + self.size_y) * 8],
                                                    fill='white')
        else:
            print(f"Instance of object {self.name} already exists, please use draw_object")

    # draws object on canvas
    def draw_object(self, canvas: Canvas):
        if self.instance is not None:
            height = int(canvas['height'])
            canvas.coords(self.instance, self.x * 8,
                          height - self.y * 8,
                          (self.x + self.size_x) * 8,
                          height - (self.y + self.size_y) * 8)
        else:
            print(f"Instance of object {self.name} does not exist, please use create_object")

    # changes object coordinates accordingly
    def move_object(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    # returns coordinates of collision followed by sides of collision (string),
    # or None, None, '' if collision didn't happen
    def collision(self, victim, speed_x, speed_y):
        speed_x = int(speed_x)
        speed_y = int(speed_y)
        victim_boundaries = [victim.x,
                             victim.y,
                             victim.x + victim.size_x,
                             victim.y + victim.size_y]
        self_boundaries = [self.x,
                           self.y,
                           self.x + self.size_x,
                           self.y + self.size_y]

        collision = [None, None]

        # loops that basically check if a vector cast from ball position to ball+speed position
        # intersects with victim object
        if abs(speed_x) > abs(speed_y):
            for i in range(0, speed_x + sgn(speed_x), sgn(speed_x)):
                # using separating axis theorem to detect rectangle collision
                if not (victim_boundaries[2] <= self_boundaries[0] + i
                        or victim_boundaries[3] <= self_boundaries[1] + round(i / float(speed_x))
                        or victim_boundaries[0] >= self_boundaries[2] + i
                        or victim_boundaries[1] >= self_boundaries[3] + round(i / float(speed_x))):
                    collision = [self_boundaries[0] + i, self_boundaries[1] + round(i / float(speed_x))]
                    break
        else:
            for i in range(0, speed_y + sgn(speed_y), sgn(speed_y)):
                # using separating axis theorem to detect rectangle collision
                if not (victim_boundaries[2] <= self_boundaries[0] + round(i / float(speed_y))
                        or victim_boundaries[3] <= self_boundaries[1] + i
                        or victim_boundaries[0] >= self_boundaries[2] + round(i / float(speed_y))
                        or victim_boundaries[1] >= self_boundaries[3] + i):
                    collision = [self_boundaries[0] + round(i / float(speed_y)), self_boundaries[1] + i]
                    break

        # check which side of victim is the collision on: lt, t, rt, r, rb, b, lb, l. l=left, t=top, r=right, b=bottom
        # this is awful
        # ... but simple
        side = ''
        if collision[0] is not None:
            distance_x = self.x - collision[0]
            distance_y = self.y - collision[1]

            # workaround of ball getting stuck in objects
            if distance_y == 0:
                distance_y = 1

            if speed_x > 0:  # not anything with r
                if speed_y > 0:  # b, lb or l
                    if collision[0] > victim.x:  # bottom
                        side = 'b'
                    elif collision[1] > victim.y:  # left
                        side = 'l'
                    else:
                        if abs(float(distance_x) / distance_y) == abs(float(speed_x) / speed_y):  # corner
                            side = 'lb'
                        elif abs(float(distance_x) / distance_y) > abs(float(speed_x) / speed_y):  # left
                            side = 'l'
                        else:  # bottom
                            side = 'b'
                else:  # l, lt or t
                    if collision[0] > victim.x:  # top
                        side = 't'
                    elif collision[1] < victim.y + victim.size_y:  # left
                        side = 'l'
                    else:
                        if abs(float(distance_x) / distance_y) == abs(float(speed_x) / speed_y):  # corner
                            side = 'lt'
                        elif abs(float(distance_x) / distance_y) > abs(float(speed_x) / speed_y):  # left
                            side = 'l'
                        else:  # top
                            side = 't'
            else:
                if speed_y > 0:  # b, rb or r
                    if collision[0] < victim.x + victim.size_x:  # bottom
                        side = 'b'
                    elif collision[1] > victim.y:  # right
                        side = 'r'
                    else:
                        if abs(float(distance_x) / distance_y) == abs(float(speed_x) / speed_y):  # corner
                            side = 'br'
                        elif abs(float(distance_x) / distance_y) > abs(float(speed_x) / speed_y):  # right
                            side = 'r'
                        else:  # bottom
                            side = 'b'
                else:  # t, rt or r
                    if collision[0] < victim.x + victim.size_x:  # top
                        side = 't'
                    elif collision[1] < victim.y + victim.size_y:  # right
                        side = 'r'
                    else:
                        if abs(float(distance_x) / distance_y) == abs(float(speed_x) / speed_y):  # corner
                            side = 'rt'
                        elif abs(float(distance_x) / distance_y) > abs(float(speed_x) / speed_y):  # right
                            side = 'r'
                        else:  # top
                            side = 't'

        return collision[0], collision[1], side
