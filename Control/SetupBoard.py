import numpy as np
from math import sqrt

from Const.VisionConst import chess_eng
from CalibrateCamera.Calibrate import *
from PLCControl.PLCControl import *
from Control.DefineChessChamp import *

#                r    h    e    a    k    a    e    h    r    c    c    p    p    p    p    p    P    P    P    P    P    C    C    R   H   E    A    K    A    E    H    R
desx = np.array([22,  61,  102, 143, 184, 225, 266, 307, 348, 61,  307, 20,  102, 184, 266, 348, 20,  102, 184, 266, 348, 61,  307, 22, 61, 102, 143, 184, 225, 266, 307, 348])
desy = np.array([387, 387, 387, 387, 387, 387, 387, 387, 387, 307, 307, 266, 266, 266, 266, 266, 143, 143, 143, 143, 143, 102, 102, 22, 20, 21,  21,  21,  21,  21,  21,  21])
desname = np.array([2, 5,  3,   0,   4,   0,   3,   5,   2,   1,   1,   6,   6,   6,   6,   6,   13,  13,  13,  13,  13,  8,   8,   9,  12, 10,  7,   11,  7,   10,  12,  9])
prio = np.array([5, 4, 5, 5, 5, 5, 3, 0, 1, 0, 0, 0, 0, 2])
min_dis_chesschamp = 25
maxint = 2000


def setup_board(chess_x_board, chess_y_board, chess_name):
    srcx, srcy, srcname = np.copy(chess_x_board), np.copy(chess_y_board), np.copy(chess_name)
    size = len(srcname)

    # arrange: danh sách từ tung độ nhỏ đến tung độ lớn
    for i in range(size - 1):
        for j in range(i + 1, size):
            if prio[srcname[j]] < prio[srcname[i]]:
                tx, ty, tn = srcx[j], srcy[j], srcname[j]
                srcx[j], srcy[j], srcname[j] = srcx[i], srcy[i], srcname[i]
                srcx[i], srcy[i], srcname[i] = tx, ty, tn

    in_right_place = []
    num_conflict_with = np.zeros(32, dtype=int)
    conflict = np.zeros((32, size), dtype=bool)
    move_conflict = []
    available_destination = np.ones(32, dtype=bool)

    def distance_s2d(src, des):
        return int(sqrt((srcx[src] - desx[des]) ** 2 + (srcy[src] - desy[des]) ** 2))

    for i in range(size):
        for j in range(32):
            # in the right place
            dis = distance_s2d(i, j)
            if (dis <= 5) and (srcname[i] == desname[j]):
                in_right_place.append(i)
                available_destination[j] = False  # des j còn trống
            # conflict: che đích
            elif (5 < dis < min_dis_chesschamp) or ((dis <= 5) and (srcname[i] != desname[j])):
                if not (i in move_conflict):
                    move_conflict.append(i)
                conflict[j, i] = True  # conflict[j, i] = True nếu src i che des j
                num_conflict_with[j] += 1  # số src che des j
    print('Số quân cờ ở đúng vị trí: ', len(in_right_place))
    for i in in_right_place:
        print(chess_eng[srcname[i]], (srcx[i], srcy[i]))
    print('Số quân cờ che điểm đến: ', len(move_conflict))
    for i in move_conflict:
        for j in range(32):
            if conflict[j, i]:
                print(chess_eng[srcname[i]], (srcx[i], srcy[i]), 'che', chess_eng[desname[j]])
    print('==============================================')

    # def make_short_list(name):
    #     if name =
    # noinspection PyShadowingNames
    def process_move(u):
        short_list = [v for v in range(size) if desname[v] == srcname[u] and available_destination[v] and num_conflict_with[v] == 0]
        # print(chess_eng[srcname[u]], short_list)
        v_save = -1
        min_dis = maxint
        for v in short_list:
            dis1 = distance_s2d(u, v)
            if dis1 < min_dis:
                min_dis = dis1
                v_save = v
        if v_save is None:
            print('Lỗi xếp cờ')
            exit()
        available_destination[v_save] = False
        in_right_place.append(u)
        print(chess_eng[srcname[u]], (srcx[u], srcy[u]), '->', (desx[v_save], desy[v_save]))
        setup_list.append((srcx[u], srcy[u], desx[v_save], desy[v_save]))

    def remove_conflict(srcmov):
        for v in range(32):
            if conflict[v, srcmov]:
                num_conflict_with[v] -= 1

    # find the first point to move
    setup_list = []

    for u in range(size):
        if srcname[u] not in [1, 6, 8, 13] and u not in in_right_place:
            remove_conflict(u)
            process_move(u)
    print('------------------------')

    for u in move_conflict:
        if u not in in_right_place:
            remove_conflict(u)  # dọn trước khi đi, tránh trường hợp chỗ mới là chỗ ngay bên cạnh mình, thì sẽ dọn chỗ đó thành trống luôn
            process_move(u)

    print('---------------------')

    for u in range(size):
        if u not in in_right_place:
            remove_conflict(u)
            process_move(u)

    if len(setup_list) == 0:
        return
    step = setup_list[0]

    opc.write(('Channel2.Device1.Y7', 0))
    home2start(step[0], step[1])
    for i in range(len(setup_list) - 1):
        step = setup_list[i]
        pick_drop(step[0], step[1], step[2], step[3])
        step2 = setup_list[i + 1]
        point2point(step[2], step[3], step2[0], step2[1])
    step = setup_list[-1]
    pick_drop(step[0], step[1], step[2], step[3])
    end2home(step[2], step[3])


"""for debugging"""
# chess_x_image, chess_y_image, chess_int = define_chess_champ()
# setup_board(chess_x_image, chess_y_image, chess_int)
