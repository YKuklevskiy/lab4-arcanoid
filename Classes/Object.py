from tkinter import Canvas


def sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


class Object:
    def __init__(self, x, y, instance=None):
        self.x = x
        self.y = y
        self.instance = instance

    name = ''
    size_x = 0
    size_y = 0

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

    def draw_object(self, canvas: Canvas):
        if self.instance is not None:
            height = int(canvas['height'])
            canvas.coords(self.instance, self.x * 8,
                          height - self.y * 8,
                          (self.x + self.size_x) * 8,
                          height - (self.y + self.size_y) * 8)
        else:
            print(f"Instance of object {self.name} does not exist, please use create_object")

    def move_object(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    # returns False, False if no collision is present,
    # or coordinates of a tile where collision occurs
    def collision(self, victim, speed_x, speed_y):
        speed_x = int(speed_x)
        speed_y = int(speed_y)
        victim_boundaries = [victim.x,
                             victim.y,
                             victim.x + victim.size_x,
                             victim.y + victim.size_y]
        self_boundaries = [self.x + speed_x,
                           self.y + speed_y,
                           self.x + self.size_x + speed_x,
                           self.y + self.size_y + speed_y]

        if speed_x > speed_y:
            for i in range(0, speed_x + sgn(speed_x), sgn(speed_x)):
                # using separating axis theorem to detect rectangle collision
                if not (victim_boundaries[2] <= self_boundaries[0] + i
                        or victim_boundaries[3] <= self_boundaries[1] + round(i/float(speed_x))
                        or victim_boundaries[0] >= self_boundaries[2] + i
                        or victim_boundaries[1] >= self_boundaries[3] + round(i/float(speed_x))):
                    return self_boundaries[0] + i, self_boundaries[1] + round(i/float(speed_x))
        else:
            for i in range(0, speed_y + sgn(speed_y), sgn(speed_y)):
                # using separating axis theorem to detect rectangle collision
                if not (victim_boundaries[2] <= self_boundaries[0] + round(i / float(speed_y))
                        or victim_boundaries[3] <= self_boundaries[1] + i
                        or victim_boundaries[0] >= self_boundaries[2] + round(i / float(speed_y))
                        or victim_boundaries[1] >= self_boundaries[3] + i):
                    return self_boundaries[0] + round(i / float(speed_y)), self_boundaries[1] + i
        return False, False
