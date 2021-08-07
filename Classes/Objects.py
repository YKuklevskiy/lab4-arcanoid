from Classes.Object import Object


class Ball(Object):
    name = 'Ball'
    size_x = 1
    size_y = 1
    movement_interval = 3  # ticks between movement
    speed = [2, 2]


class Racket(Object):
    name = 'Racket'
    size_x = 14
    size_y = 1
    movement_interval = 1
    speed = 1


class Block(Object):
    name = 'Block'
    size_x = 10
    size_y = 3
