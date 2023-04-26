import numpy as np
from math import sqrt
from Const.VisionConst import chess_eng
from CalibrateCamera.Calibrate import *
from PLCControl.PLCControl import *

from DefineChessChamp import *

#                r   h   e    a    k    a    e    h    r    c   c    p    p    p    p    p    P    P    P    P    P    C    C    R    H    E    A    K    A    E    H    R
desx = np.array(
    [20, 61, 102, 143, 184, 225, 266, 307, 348, 61, 307, 20, 102, 184, 266, 348, 20, 102, 184, 266, 348, 61, 307, 20,
     61, 102, 143, 184, 225, 266, 307, 348])
desy = np.array(
    [20, 20, 20, 20, 20, 20, 20, 20, 20, 102, 102, 143, 143, 143, 143, 143, 266, 266, 266, 266, 266, 307, 307, 389, 389,
     389, 389, 389, 389, 389, 389, 389])
desname = np.array(
    [2, 5, 3, 0, 4, 0, 3, 5, 2, 1, 1, 6, 6, 6, 6, 6, 13, 13, 13, 13, 13, 8, 8, 9, 12, 10, 7, 11, 7, 10, 12, 9])
min_dis_chesschamp = 34

maxint = 2000

prio = np.array([0, 1, 0, 0, 0, 0, 2, 5, 4, 5, 5, 5, 5, 3])


def setup_board(chess_x_image, chess_y_image, chess_int):
    chess_x = np.round(width_real / image_width * chess_x_image, 1)
    chess_y = np.round(-1 * height_real / image_height * (chess_y_image - image_height), 1)
    srcx, srcy = fix_real(chess_x, chess_y)
    srcname = np.copy(chess_int)
    size = len(chess_int)

    # arrange: danh sách từ tung độ nhỏ đến tung độ lớn
    for i in range(size - 1):
        for j in range(i + 1, size):
            if prio[srcname[j]] < prio[srcname[i]]:
                tx, ty, tn = srcx[j], srcy[j], srcname[j]
                srcx[j], srcy[j], srcname[j] = srcx[i], srcy[i], srcname[i]
                srcx[i], srcy[i], srcname[i] = tx, ty, tn

    right_place = []
    num_conflict = np.zeros(32, dtype=int)
    conflict = np.zeros((32, size), dtype=bool)
    move_first = []
    available = np.ones(32, dtype=bool)

    def distance_s2d(src, des):
        return int(sqrt((srcx[src] - desx[des]) ** 2 + (srcy[src] - desy[des]) ** 2))

    for i in range(size):
        for j in range(32):
            # in the right place
            dis = distance_s2d(i, j)
            if (dis <= 5) and (srcname[i] == desname[j]):
                right_place.append(i)
                available[j] = False  # des j còn trống
            # conflict: che đích
            elif (5 < dis < min_dis_chesschamp) or ((dis <= 5) and (srcname[i] != desname[j])):
                # and (srcname[i] != desname[j]):
                if not (i in move_first):
                    move_first.append(i)
                conflict[j, i] = True  # conflict[j, i] = True nếu src i che des j
                num_conflict[j] += 1  # số src che des j
    print('Số quân cờ ở đúng vị trí: ', len(right_place))
    for i in right_place:
        print(chess_eng[srcname[i]], (srcx[i], srcy[i]))
    print('Số quân cờ che điểm đến: ', len(move_first))
    for i in move_first:
        for j in range(32):
            if conflict[j, i]:
                print(i, chess_eng[srcname[i]], (srcx[i], srcy[i]), 'che', chess_eng[desname[j]])
    print('==============================================')

    def process_move(u):
        # v_save = 0
        short_list = []
        for v in range(32):
            if desname[v] == srcname[u] and available[v] \
                    and (num_conflict[v] == 0 or (num_conflict[v] == 1 and conflict[v, u])):
                # hoàn toàn tự do và trống trải hoặc chỉ bị cản bởi mỗi mình quân thuộc về ô đó
                short_list.append(v)
        print(chess_eng[srcname[u]], short_list)
        min_dis = maxint
        for v in short_list:
            dis1 = distance_s2d(u, v)
            if dis1 < min_dis:
                min_dis = dis1
                v_save = v
        available[v_save] = False
        right_place.append(u)
        print(chess_eng[srcname[u]], (srcx[u], srcy[u]), '->', (desx[v_save], desy[v_save]))
        setup_list.append((srcx[u], srcy[u], desx[v_save], desy[v_save]))

    def remove_conflict(srcmov):
        for v in range(32):
            if conflict[v, srcmov]:
                num_conflict[v] -= 1

    # find the first point to move
    setup_list = []
    # danger = np.zeros(size)
    # for u in move_first:
    #     for v in range(32):
    #         if conflict[v, u]:
    #             danger[u] += 1
    # for i in range(len(move_first)-1):
    #     for j in range(len(move_first)):
    #         if danger[move_first[i]] < danger[move_first[j]]:
    #             tmp = move_first[i]
    #             move_first[i] = move_first[j]
    #             move_first[j] = tmp

    for u in move_first:
        process_move(u)
        remove_conflict(u)
    print('---------------------')

    for u in range(size):
        if u not in right_place:
            process_move(u)
            remove_conflict(u)

    step = setup_list[0]
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
