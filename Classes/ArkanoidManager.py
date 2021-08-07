from Classes.Objects import *
from tkinter import Canvas, Tk, Label
from time import sleep

arrow_keys_state = [False, False]


# Class for managing game flow
class ArkanoidManager:
    def __init__(self, window: Tk, canvas: Canvas, score: Label, status: Label,
                 ball: Ball, racket: Racket, blocks: list):
        self.window = window
        self.canvas = canvas
        self.ball = ball
        self.racket = racket
        self.blocks = blocks
        self.score = score
        self.status = status
        self.game_start_ticks = 50  # how many ticks will pass before the start of the game
        self.blocks_count = len(self.blocks)  # initial quantity of blocks
        self.field = [int(canvas['width']) / 8, int(canvas['height']) / 8]  # block-measurements for game field

    # called on any key pressed
    @staticmethod
    def key_pressed(event):
        if event.keysym == 'Left':
            arrow_keys_state[0] = True
        elif event.keysym == 'Right':
            arrow_keys_state[1] = True

    # called on any key stopped being pressed
    @staticmethod
    def key_released(event):
        if event.keysym == 'Left':
            arrow_keys_state[0] = False
        elif event.keysym == 'Right':
            arrow_keys_state[1] = False

    # initializes objects and properties
    def initialize(self):
        self.ball.create_object(self.canvas)
        self.racket.create_object(self.canvas)
        for block in self.blocks:
            block.create_object(self.canvas)
        self.window.bind('<Key>', self.key_pressed)
        self.window.bind('<KeyRelease>', self.key_released)
        self.loop()  # starts the game

    # draws all objects
    def draw_frame(self):
        self.ball.draw_object(self.canvas)
        self.racket.draw_object(self.canvas)
        for block in self.blocks:
            block.draw_object(self.canvas)

    # updates scoreboard and checks if all the blocks vere destroyed
    def update_score(self):
        self.score.configure(text=f'Score: {str((self.blocks_count - len(self.blocks)) * 100).zfill(3)}')
        if len(self.blocks) == 0:
            self.ball.speed = [0, 0]

    # initiates game-over game state
    def game_over(self):
        self.status.configure(text='GAME OVER')

    # initiates victory game state
    def victory(self):
        self.status.configure(text='VICTORY!', fg='green')

    # for managing tick-like movement of ball and racket
    mv_intervals = [0, 0]  # [ball_ticks, racket_ticks]

    def ball_movement(self):
        if self.mv_intervals[0] >= self.ball.movement_interval - 1:  # ready to move
            x, y = self.check_collisions()
            self.ball.move_object(x, y)
            self.mv_intervals[0] = 0
        else:  # wait a tick
            self.mv_intervals[0] += 1

    # get collision info and deltas, handle the collision and return resulting deltas
    def calc_ball_collision(self, collision: tuple[int, int, str], collision_direction, delta_x, delta_y):
        if collision[2].find('r') != -1:  # right-side (victim) collision
            delta_x = int((collision[0] + 1 - self.ball.x - delta_x) - (self.ball.x - collision[0] - 1))
            collision_direction[0] = not collision_direction[0]
        if collision[2].find('l') != -1:  # left-side (victim) collision
            delta_x = int((collision[0] - self.ball.x - delta_x - self.ball.size_x)
                          + (collision[0] - self.ball.x - self.ball.size_x))
            collision_direction[2] = not collision_direction[2]
        if collision[2].find('t') != -1:  # top (victim) collision
            delta_y = (int(collision[1]) + 1 - self.ball.y - delta_y) \
                      - (self.ball.y - int(collision[1]) - 1)
            collision_direction[3] = not collision_direction[3]
        if collision[2].find('b') != -1:  # bottom (victim) collision
            delta_y = (collision[1] - self.ball.y - delta_y - self.ball.size_y) \
                      + (collision[1] - self.ball.y - self.ball.size_y)
            collision_direction[1] = not collision_direction[1]

        return delta_x, delta_y

    # check and handle all frame collisions, return final ball displacement
    def check_collisions(self):
        speed = self.ball.speed
        delta_x = speed[0]
        delta_y = speed[1]
        collision_direction = [False, False, False, False]  # left, up, right, down

        # check racket collision
        racket_collision = self.ball.collision(self.racket, speed[0], speed[1])
        if racket_collision[0] is not None:

            delta_x, delta_y = self.calc_ball_collision(racket_collision, collision_direction, delta_x, delta_y)

            # change the ball velocity if the racket is moving
            if arrow_keys_state[0]:
                self.ball.speed[0] -= self.racket.speed
            if arrow_keys_state[1]:
                self.ball.speed[0] += self.racket.speed

        # check blocks collision
        all_blocks_checked = False
        while not all_blocks_checked:
            all_blocks_checked = True
            i = 0
            while i < len(self.blocks):
                if delta_x == delta_y == 0:  # if ball already moved as much as it could
                    all_blocks_checked = True
                    break
                block_collision = self.ball.collision(self.blocks[i], delta_x, delta_y)
                if block_collision[0] is not None:  # collision with a block
                    all_blocks_checked = False
                    delta_x, delta_y = self.calc_ball_collision(block_collision, collision_direction, delta_x, delta_y)

                    # deleting the crushed block, updating score table
                    self.canvas.delete(self.blocks[i].instance)
                    del self.blocks[i]
                    i -= 1
                i += 1

        # check wall collision
        if delta_x > 0:
            if self.ball.x + delta_x + self.ball.size_x > self.field[0]:  # right collision
                delta_x = (self.field[0] - self.ball.x - delta_x - self.ball.size_x) \
                          + (self.field[0] - self.ball.x - self.ball.size_x)
                collision_direction[2] = not collision_direction[2]
        else:
            if self.ball.x + delta_x < 0:  # left collision
                delta_x = (-self.ball.x - delta_x) - self.ball.x
                collision_direction[0] = not collision_direction[0]
        if delta_y > 0:
            if self.ball.y + delta_y + self.ball.size_y > self.field[1]:  # up collision
                delta_y = (self.field[1] - self.ball.y - delta_y - self.ball.size_y) \
                          + (self.field[1] - self.ball.y - self.ball.size_y)
                collision_direction[1] = not collision_direction[1]
        else:
            if self.ball.y + delta_y < 0:  # down collision, loss
                # delta_y = (-self.ball.y - delta_y) - self.ball.y
                # collision_direction[3] = not collision_direction[3]
                self.ball.speed = [0, 0]

        # changing ball speed if it was reversed by collisions in any way
        if collision_direction[0] != collision_direction[2]:
            self.ball.speed[0] *= -1
        if collision_direction[1] != collision_direction[3]:
            self.ball.speed[1] *= -1

        return delta_x, delta_y

    def racket_movement(self):
        if self.mv_intervals[1] >= self.racket.movement_interval - 1:  # ready to move
            if arrow_keys_state[0] != arrow_keys_state[1]:
                if arrow_keys_state[0]:
                    if self.racket.x - self.racket.speed < 0:  # left field border
                        self.racket.x = 0
                    else:
                        self.racket.move_object(-self.racket.speed, 0)
                else:
                    if self.racket.x + self.racket.speed + self.racket.size_x > self.field[0]:  # right field border
                        self.racket.x = self.field[0] - self.racket.size_x
                    else:
                        self.racket.move_object(self.racket.speed, 0)
            self.mv_intervals[1] = 0
        else:  # wait a tick
            self.mv_intervals[1] += 1

    # all calculations per frame
    def calculate(self):
        self.racket_movement()
        self.ball_movement()

    _TICK = 10  # time between frames

    # game cycle
    def loop(self):
        if self.game_start_ticks <= 0:
            self.calculate()
            self.update_score()
            self.draw_frame()
        else:
            self.game_start_ticks -= 1

        # check for game state changes, if not - continue game cycle
        if self.ball.speed != [0, 0]:
            self.window.after(self._TICK, self.loop)
        else:
            if len(self.blocks) == 0:
                self.victory()
            else:
                self.game_over()
