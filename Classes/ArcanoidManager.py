from Classes.Objects import *


# Class for managing game flow
class ArcanoidManager:
    def __init__(self, canvas, ball, paddle, blocks):
        self.canvas = canvas
        self.ball = ball
        self.paddle = paddle
        self.blocks = blocks
