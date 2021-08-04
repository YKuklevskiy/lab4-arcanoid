# Написать примитивного арканоида, должна быть управляемая каретка и движущийся шарик и границы,
# для каждого также будут дополнительные фигуры, взять их можно у меня.
# Задание на 2 плюса: Сделать наверху 6 ячеек, которые при попадании мячика будут исчезать.

from tkinter import *
from Classes.ArcanoidManager import ArcanoidManager
from Classes.Objects import *

window = Tk()
window.title('Arcanoid')

canvas = Canvas(window, width=1000, height=600, bg='black') # as a tile is 8x8, the field is 125*75

canvas.pack()
ball_instance = canvas.create_rectangle(8, 8, 16, 16, fill='white')

ball = Ball(1, 1, ball_instance)

# cur_coords = canvas.coords(ball)
# canvas.coords(ball, cur_coords[0]+8, cur_coords[1]+8, cur_coords[2]+8, cur_coords[3]+8)

window.mainloop()

