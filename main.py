# Написать примитивного арканоида, должна быть управляемая каретка и движущийся шарик и границы,
# для каждого также будут дополнительные фигуры, взять их можно у меня.
# Задание на 2 плюса: Сделать наверху 6 ячеек, которые при попадании мячика будут исчезать.

from tkinter import *
from Classes.ArkanoidManager import ArkanoidManager
from Classes.Objects import *

window = Tk()
window.title('Arkanoid')

# as a tile is 8x8, the field is 125*75
canvas = Canvas(window, width=1000, height=600, bg='black', highlightthickness=0)
canvas.grid(column=0, row=0)

ball = Ball(62, 36)

racket = Racket(1, 0)

blocks = list()

BLOCK_START_POS_X = 12
BLOCK_START_POS_Y = 60
for i in range(3):
    for j in range(14):
        blocks.append(Block(BLOCK_START_POS_X + j * (Block.size_x + 2), BLOCK_START_POS_Y + i * (Block.size_y + 2)))

manager = ArkanoidManager(window, canvas, ball, racket, blocks)
manager.initialize()

window.mainloop()
