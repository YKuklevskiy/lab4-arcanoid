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

    # check collision, return final ball displacement
    def check_collision(self):
        speed = self.ball.speed
        delta_x = speed[0]
        delta_y = speed[1]
        collision_direction = [False, False, False, False]  # left, up, right, down

        # check racket collision
        if self.ball.collides(self.racket, speed[0], speed[1]):
            if arrow_keys_state[0]:
                self.ball.speed[0] -= self.racket.speed
            if arrow_keys_state[1]:
                self.ball.speed[0] += self.racket.speed

            collision_x, collision_y = self.ball.collision(self.racket, self.ball.speed[0], self.ball.speed[1])
            if type(collision_x) != type(bool):
                ball_velocity = (self.ball.speed[0]**2+self.ball.speed[1]**2)**0.5
                collision_distance = ((self.ball.x-collision_x)**2+(self.ball.y-collision_y)**2)**0.5
                angle = (self.ball.y-collision_y)/collision_distance
                # calculations wrong, bottom left border of ball doesn't collide with bottom left border of object
                # have to account

            # if not upper racket collision or corner collision, then ball always bounces down to its doom
            # thus no reason to check side collision

            # difficulties in handling collision: is it corner collision,
            # which way and how far will the collision send ball, etc
            # it would be better to create a class just for handling collisions,
            # this will improve code readability and make things easier

            # if side collision, only one delta changes, if corner - both deltas change, the most easy way to do
            # all that is to create a function returning new delta coords in collision class (as objects are rectangles)

            #
            # # check if upper bound collision
            # distance_y = self.ball.y - self.racket.y - self.racket.size_y
            # if self.ball.x >= self.racket.x + self.racket.size_x:
            #     distance_x = self.ball.x - self.racket.x - self.racket.size_x
            #     if float(distance_x)/distance_y == abs(float(speed[0])/speed[1]):  # corner collision
            #         delta_x = (self.racket.x + self.racket.size_x - self.ball.x + delta_x)\
            #                   - (self.ball.x - self.racket.x - self.racket.size_x)
            #         collision_direction[0] = True
            #
            # elif self.ball.x <= self.racket.x:
            #     distance_x = self.racket.x - self.ball.x - self.ball.size_x
            #     if

        # check blocks collision

        # check wall collision
        if delta_x > 0:
            if self.ball.x + delta_x + self.ball.size_x > self.field[0]:  # right collision
                delta_x = (self.field[0] - self.ball.x - delta_x - self.ball.size_x)\
                          + (self.field[0] - self.ball.x - self.ball.size_x)
                collision_direction[2] = not collision_direction[2]
        else:
            if self.ball.x + delta_x < 0:  # left collision
                delta_x = (-self.ball.x - delta_x) - self.ball.x
                collision_direction[0] = not collision_direction[0]
        if delta_y > 0:
            if self.ball.y + delta_y + self.ball.size_y > self.field[1]:  # up collision
                delta_y = (self.field[1] - self.ball.y - delta_y - self.ball.size_y)\
                          + (self.field[1] - self.ball.y - self.ball.size_y)
                collision_direction[1] = not collision_direction[1]
        else:
            if self.ball.y + delta_y < 0:  # down collision
                delta_y = (-self.ball.y - delta_y) - self.ball.y
                collision_direction[3] = not collision_direction[3]

        if collision_direction[0] != collision_direction[2]:
            self.ball.speed[0] *= -1
        if collision_direction[1] != collision_direction[3]:
            self.ball.speed[1] *= -1

        return delta_x, delta_y
        pass

    def racket_movement(self):
        if self.mv_intervals[1] >= self.racket.movement_interval - 1:  # ready to move
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
            self.mv_intervals[1] = 0
        else:  # wait a tick
            self.mv_intervals[1] += 1

    def calculate(self):
        self.racket_movement()
        self.ball_movement()
        pass

    _TICK = 10  # time between frames

    def loop(self):
        self.calculate()

        self.draw_frame()
        self.window.after(self._TICK, self.loop)
