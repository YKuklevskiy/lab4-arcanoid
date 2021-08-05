from Classes.Object import Object

class Collision:
    def __init__(self, x, y, collision_type='flat'):
        self.x = x
        self.y = y
        self.collision_type = collision_type
