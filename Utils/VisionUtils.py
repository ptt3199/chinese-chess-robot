import cv2
import numpy as np

from Const.VisionConst import *


def convert_binary(image, thresh=130, show=False):
    _, image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    if show:
        cv2.imshow("Binary image", image)
        cv2.waitKey(100)
        cv2.destroyAllWindows()
    return image


def matrix2fen(matrix):
    """
    matrix2fen: translate 2d matrix to fen string
    @param: a fen string
    @return: 2d matrix correspond with fen string
    """
    fen = ""
    count_row = 0
    for row in matrix:
        i = 0
        count_row += 1
        for e in row:
            if e == '.':
                i += 1
            elif i != 0:
                fen += str(i)
                fen += e
                i = 0
            else:
                fen += e
        if i != 0:
            fen += str(i)
        if count_row != 10:
            fen += '/'
    return fen


def fen2matrix(fen):
    """
    fen2matrix: translate fen string to matrix 2 dimension
    @param: a fen string
    @return: 2d matrix correspond with fen string
    """
    state = np.array(
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.'])
    i = 0
    for e in fen:
        if e in NUMSTRING:
            i += int(e)
        elif e in CHESSMAN:
            state[i] = e
            i += 1
    state = state.reshape(10, 9)
    # print(state)
    return state


def fen2matrix_cn(fen, mov):
    """
    fen2matrix: translate fen string to matrix 2 dimension
    @param: a fen string
    @return: 2d matrix correspond with fen string
    """
    state = np.array(
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
         '.', '.', '.', '.', '.', '.'])
    i = 0
    for e in fen:
        if e in NUMSTRING:
            i += int(e)
        elif e in CHESSMAN:
            state[i] = e
            i += 1
    src_x, src_y, dst_x, dst_y = move_in_state(mov)
    state2d = state.reshape(10, 9)
    state2d[src_x][src_y] = '*'
    # state2d[dst_x][dst_y] = '[' + state2d[dst_x][dst_y]
    print(state2d)


def move_in_state(mv):
    src = mv & 255
    dst = mv >> 8
    src_x = int(src / 16) - 3
    src_y = int(src % 16) - 3
    dst_x = int(dst / 16) - 3
    dst_y = int(dst % 16) - 3
    return src_x, src_y, dst_x, dst_y
