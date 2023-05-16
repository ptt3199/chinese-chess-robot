
"""===================== Homemade library ===================="""
from GUI_SettingMenu import *
from Control.PlayChess import *
from Control.SetupBoard import *
from Control.SetInitialState import *
from Const.VisionConst import *

"""==========================================================="""
go_first, level = get_setting()


opc.write(('Channel2.Device1.Y11', 0))
opc.write(('Channel2.Device1.Y7', 1))
"""==========================================================="""
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


def set_initial_state_button():
    global previous_fen
    cv2.imwrite('.\\Camera\\temp.jpg', input_image)
    cx, cy, cname = define_chess_champ()
    previous_fen = set_initial_state(cx, cy, cname)
    opc.write(('Channel2.Device1.Y7', 1))


initial_button = Button(liveCamWindow, text='Set Initial State', command=set_initial_state_button)
initial_button.pack()


def setup_board_button():
    cv2.imwrite('.\\Camera\\temp.jpg', input_image)
    cx, cy, cname = define_chess_champ()
    setup_board(cx, cy, cname)


setup_button = Button(liveCamWindow, text='Setup Chessboard', command=setup_board_button)
setup_button.pack()

previous_fen = ''


def take_turn_button():
    # noinspection PyGlobalUndefined
    global previous_fen, go_first
    opc.write(('Channel2.Device1.Y7', 0))  # tắt đèn vàng báo đã bấm nút
    cv2.imwrite('.\\Camera\\temp.jpg', input_image)
    cx, cy, cname = define_chess_champ()
    if go_first == 2:
        if previous_fen == '':
            previous_fen = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR'
        previous_fen = play_chess_1_time_robot_first(previous_fen, cx, cy, cname, level)
        go_first = 1
    if previous_fen == '':
        previous_fen = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR'
    previous_fen = play_chess(previous_fen, cx, cy, cname, level)


turn_button = Button(liveCamWindow, text='Your turn', command=take_turn_button)
turn_button.pack()

photo, input_image = None, None

pressLabel = Label(liveCamWindow, text='')


def update_frame():
    global canvas, photo, input_image, green_button, yellow_button
    _, frame = capture.read()
    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    shown_image = input_image

    frame = cv2.resize(shown_image, dsize=None, fx=1 / 3, fy=1 / 3)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    gb = check_green_button()
    if green_button != gb:
        green_button = gb
        print('Setup Button pressed')
        setup_board_button()
    yb = check_yellow_button()
    if yellow_button != yb:
        yellow_button = yb
        print('Turn Button pressed')
        take_turn_button()

    liveCamWindow.after(1, update_frame)


green_button = check_green_button()
yellow_button = check_yellow_button()
update_frame()
liveCamWindow.mainloop()
