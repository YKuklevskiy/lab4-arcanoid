from Classes.Object import Object


class Ball(Object):
    name = 'Ball'
    size_x = 1
    size_y = 1
    movement_interval = 10  # ticks between movement
    speed = [1, 1]


class Racket(Object):
    name = 'Racket'
    size_x = 10
    size_y = 1
    movement_interval = 1
    speed = 1


class Block(Object):
    name = 'Block'
    size_x = 6
    size_y = 2
