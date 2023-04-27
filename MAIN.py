import cv2
import numpy as np
import tkinter

from tkinter import *
from tkinter.ttk import *

"""===================== Homemade library ===================="""
from GUI_SettingMenu import *

# from PLCControl.PLCControl import *
#
from DefineChessChamp import *
# from PlayChess import *
from SetupBoard import *

# client_engine = Client(8080)
"""==========================================================="""
# go_first, game_type, level = get_setting()
# print(go_first)
# print(game_type)
# print(level)


liveCamWindow = Tk()
liveCamWindow.title('Live camera')

"""Capture live"""
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

canvas_h = capture.get(cv2.CAP_PROP_FRAME_HEIGHT) // 3
canvas_w = capture.get(cv2.CAP_PROP_FRAME_WIDTH) // 3
canvas = Canvas(liveCamWindow, height=canvas_h, width=canvas_w)
canvas.pack()


def setup_board_button():
    cv2.imwrite('.\\Camera\\temp.jpg', input_image)
    chess_x_image, chess_y_image, chess_int = define_chess_champ()
    setup_board(chess_x_image, chess_y_image, chess_int)


setup_button = Button(liveCamWindow, text='Setup Chessboard', command=setup_board_button)
setup_button.pack()


def take_turn_button():
    cv2.imwrite('.\\Camera\\temp.jpg', input_image)
    chess_x_image, chess_y_image, chess_int = define_chess_champ()
    play_chess(chess_x_image, chess_y_image, chess_int)


turn_button = Button(liveCamWindow, text='Your turn', command=take_turn_button)
turn_button.pack()

photo, input_image = None, None

pressLabel = Label(liveCamWindow, text='')


def update_frame():
    global canvas, photo, input_image
    _, frame = capture.read()
    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(input_image, dsize=None, fx=1 / 3, fy=1 / 3)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    green_button = check_green_button()
    yellow_button = check_yellow_button()

    if green_button != check_green_button():
        print('Setup Button pressed')
        setup_board_button()

    if yellow_button != check_yellow_button():
        opc.write(('Channel2.Device1.Y7', 0))
        print('Turn Button pressed')
        take_turn_button()

    liveCamWindow.after(1, update_frame)


update_frame()
liveCamWindow.mainloop()
