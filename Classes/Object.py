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
        if self.instance is not None:
            self.instance = canvas.create_rectangle(self.x * 8,
                                                    canvas.winfo_height() - self.y * 8,
                                                    (self.x + self.size_x) * 8,
                                                    canvas.winfo_height() - (self.y + self.size_y) * 8)
        else:
            print(f"Instance of object {self.name} already exists, please use place_object")

    def draw_object(self, canvas: Canvas):
        canvas.coords(self.instance, self.x * 8,
                      canvas.winfo_height() - self.y * 8,
                      (self.x + self.size_x) * 8,
                      canvas.winfo_height() - (self.y + self.size_y) * 8)

    def move_object(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
