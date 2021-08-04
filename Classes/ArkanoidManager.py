from Classes.Objects import *
from tkinter import Canvas, Tk

arrow_keys_state = [False, False]


# Class for managing game flow
class ArkanoidManager:
    def __init__(self, window: Tk, canvas: Canvas, ball: Ball, racket: Racket, blocks: list):
        self.window = window
        self.canvas = canvas
        self.ball = ball
        self.racket = racket
        self.blocks = blocks
        self.ball.create_object(self.canvas)
        self.racket.create_object(self.canvas)
        self.field = [int(canvas['width']) / 8, int(canvas['height']) / 8]
        for block in self.blocks:
            block.create_object(self.canvas)

    @staticmethod
    def key_pressed(event):
        if event.keysym == 'Left':
            arrow_keys_state[0] = True
        elif event.keysym == 'Right':
            arrow_keys_state[1] = True

    @staticmethod
    def key_released(event):
        if event.keysym == 'Left':
            arrow_keys_state[0] = False
        elif event.keysym == 'Right':
            arrow_keys_state[1] = False

    def initialize(self):
        self.window.bind('<Key>', self.key_pressed)
        self.window.bind('<KeyRelease>', self.key_released)
        self.loop()

    def draw_frame(self):
        self.ball.draw_object(self.canvas)
        self.racket.draw_object(self.canvas)
        for block in self.blocks:
            block.draw_object(self.canvas)

    mv_intervals = [0, 0]  # 1st - ball, 2nd - paddle

    def ball_movement(self):  # todo add speed boost from racket
        if self.mv_intervals[0] >= self.ball.movement_interval - 1:  # ready to move
            x, y = self.check_collision()
            self.ball.move_object(x, y)
            self.mv_intervals[0] = 0
        else:  # wait a tick
            self.mv_intervals[0] += 1

    def check_collision(self):
        delta_x = 0
        delta_y = 0
        # check collision, return final ball displacement
        return delta_x, delta_y
        pass

    def racket_movement(self):
        if arrow_keys_state[0] != arrow_keys_state[1]:
            if arrow_keys_state[0]:
                if self.racket.x - self.racket.speed < 0:
                    self.racket.x = 0
                else:
                    self.racket.move_object(-self.racket.speed, 0)
            else:
                if self.racket.x + self.racket.speed + self.racket.size_x > self.field[0]:
                    self.racket.x = self.field[0] - self.racket.size_x
                else:
                    self.racket.move_object(self.racket.speed, 0)

    def calculate(self):
        self.racket_movement()
        # self.ball_movement()
        pass

    _TICK = 20  # time between frames

    def loop(self):
        self.calculate()

        self.draw_frame()
        self.window.after(self._TICK, self.loop)
