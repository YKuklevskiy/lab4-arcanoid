# Написать примитивного арканоида, должна быть управляемая каретка и движущийся шарик и границы,
# для каждого также будут дополнительные фигуры, взять их можно у меня.
# Задание на 2 плюса: Сделать наверху 6 ячеек, которые при попадании мячика будут исчезать.

from tkinter import *
from Classes.ArkanoidManager import ArkanoidManager
from Classes.Objects import *
import tkinter.font as tkFont

window = Tk()
window.title('Arkanoid')
window.configure(bg='#303030')
window.resizable(0, 0)

# main frame for score and status labels
stats_frame = Frame(window)

# print('\n'.join(tkFont.families()))
font = tkFont.Font(family='Eras Demi ITC', size=18, weight='bold')

# score frame setup
score_label = Label(stats_frame, font=font, text='Score: 000', fg='white', bg='#303030')
status_label = Label(stats_frame, font=font, text='', fg='red', bg='#303030')
status_label.grid(column=0, row=0, ipadx=50)
score_label.grid(column=2, row=0, sticky=W, ipadx=50)
Grid.columnconfigure(stats_frame, 1, weight=1)
Grid.columnconfigure(stats_frame, 0, weight=1)
stats_frame.grid(column=0, row=0)

# as a tile is 8x8, the field is 125*75
canvas = Canvas(window, width=1000, height=600, bg='black', highlightthickness=0)
canvas.grid(column=0, row=1)

ball = Ball(45, 2)

racket = Racket(40, 0)

blocks = list()

# starting position for block-field
BLOCK_START_POS_X = 14
BLOCK_START_POS_Y = 45
for i in range(3):
    for j in range(7):
        blocks.append(Block(BLOCK_START_POS_X + j * (Block.size_x + 4), BLOCK_START_POS_Y + i * (Block.size_y + 4)))

manager = ArkanoidManager(window, canvas, score_label, status_label, ball, racket, blocks)
manager.initialize()

window.mainloop()
