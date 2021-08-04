from Classes.Objects import *
from tkinter import Canvas, Tk
import time


# Class for managing game flow
class ArkanoidManager:
    def __init__(self, window: Tk, canvas: Canvas, ball, paddle, blocks):
        self.window = window
        self.canvas = canvas
        self.ball = ball
        self.paddle = paddle
        self.blocks = blocks
        self.ball.create_object(self.canvas)
        self.paddle.create_object(self.canvas)
        for block in self.blocks:
            block.create_object(self.canvas)

    def draw_frame(self):
        self.ball.draw_object(self.canvas)
        self.paddle.draw_object(self.canvas)
        for block in self.blocks:
            block.draw_object(self.canvas)

    def calculate(self):
        pass

    _TICK = 50  # time between frames

    def loop(self):
        self.calculate()

        self.draw_frame()
        self.window.after(self._TICK, self.loop)
