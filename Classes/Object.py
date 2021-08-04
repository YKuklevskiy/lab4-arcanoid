from tkinter import Canvas


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
