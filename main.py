# Написать примитивного арканоида, должна быть управляемая каретка и движущийся шарик и границы,
# для каждого также будут дополнительные фигуры, взять их можно у меня.
# Задание на 2 плюса: Сделать наверху 6 ячеек, которые при попадании мячика будут исчезать.

from tkinter import *
from Classes.ArcanoidManager import ArcanoidManager
from Classes.Objects import *

window = Tk()
window.title('Arcanoid')

# as a tile is 8x8, the field is 125*75
canvas = Canvas(window, width=1000, height=600, bg='black', highlightthickness=0)
canvas.grid(column=0, row=0)

ball = Ball(62, 36)
ball.create_object(canvas)

paddle = Paddle(1, 0)
paddle.create_object(canvas)

# print(canvas.coords(ball.instance)) # for debug

window.mainloop()
