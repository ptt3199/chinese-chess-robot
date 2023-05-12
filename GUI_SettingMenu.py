import cv2
import PIL.Image
import PIL.ImageTk
import tkinter

from tkinter import *
from tkinter.ttk import *

go_first, game_type, level = 0, 0, 0


# noinspection PyUnboundLocalVariable
def get_setting():
    welcomeWindow = Tk()
    welcomeWindow.title('Game Setting')

    def sel1(i):
        global go_first
        go_first = i

    label = tkinter.Label(welcomeWindow, text='WHO GO FIRST')
    label.grid(column=0, row=0, sticky=W)
    var = IntVar()
    button = Radiobutton(welcomeWindow, text='Player', variable=var, value=1, command=lambda value=1: sel1(1))
    button.grid(column=1, row=0, sticky=W)
    button = Radiobutton(welcomeWindow, text='Computer', variable=var, value=2, command=lambda value=2: sel1(2))
    button.grid(column=2, row=0, sticky=W)

    # def sel2(i):
    #     global game_type
    #     game_type = i
    #
    # label = tkinter.Label(welcomeWindow, text='GAME TYPE')
    # label.grid(column=0, row=1, sticky=W)
    # var = IntVar()
    # button = Radiobutton(welcomeWindow, text='Classic', variable=var, value=1, command=lambda value=1: sel2(1))
    # button.grid(column=1, row=1, sticky=W)
    # button = Radiobutton(welcomeWindow, text='Challenging', variable=var, value=2, command=lambda value=2: sel2(2))
    # button.grid(column=2, row=1, sticky=W)

    def sel3(i):
        global level
        level = i

    label = tkinter.Label(welcomeWindow, text='LEVEL')
    label.grid(column=0, row=2, sticky=W)
    var = IntVar()
    button = Radiobutton(welcomeWindow, text='Easy', variable=var, value=1, command=lambda value=1: sel3(1))
    button.grid(column=1, row=2, sticky=W)
    button = Radiobutton(welcomeWindow, text='Medium', variable=var, value=2, command=lambda value=2: sel3(2))
    button.grid(column=2, row=2, sticky=W)
    button = Radiobutton(welcomeWindow, text='Hard', variable=var, value=3, command=lambda value=3: sel3(3))
    button.grid(column=3, row=2, sticky=W)

    def cli():
        if go_first != 0 and game_type != 0 or level != 0:
            welcomeWindow.destroy()

    button = Button(welcomeWindow, text='Start game', command=cli)
    button.grid(column=3, row=3, sticky=W)

    welcomeWindow.mainloop()

    return go_first, level
