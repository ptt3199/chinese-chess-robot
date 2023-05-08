"""===================== Homemade library ===================="""
from GUI_SettingMenu import *
from Control.PlayChess import *
from Control.SetupBoard import *
from Const.VisionConst import *

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
    cx, cy, cname = define_chess_champ()
    setup_board(cx, cy, cname)


setup_button = Button(liveCamWindow, text='Setup Chessboard', command=setup_board_button)
setup_button.pack()

previous_fen = ''


def take_turn_button():
    global previous_fen
    opc.write(('Channel2.Device1.Y7', 0))
    cv2.imwrite('.\\Camera\\temp.jpg', input_image)
    cx, cy, cname = define_chess_champ()
    if previous_fen == '':
        previous_fen = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR'
        # previous_fen = 'rh1ak1er1/1R2a4/4e1h2/p1p5p/6p2/C8/P1P1H1P1P/1C7/8R/2EAKAE2'
    previous_fen = play_chess(previous_fen, cx, cy, cname)


turn_button = Button(liveCamWindow, text='Your turn', command=take_turn_button)
turn_button.pack()

photo, input_image = None, None

pressLabel = Label(liveCamWindow, text='')


def update_frame():
    global canvas, photo, input_image, green_button, yellow_button
    _, frame = capture.read()
    input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    shown_image = input_image
    # shown_image = calibrate_remap_image(input_image)
    # left, right, top, bottom = raw_left, raw_right, raw_top, raw_bottom
    # shown_image = shown_image[top:bottom, left:right]  # Remove leftovers

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
