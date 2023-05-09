from Control.ValidateState import *


def set_initial_state(chess_x_board, chess_y_board, chess_name):
    srcx, srcy, srcname = np.copy(chess_x_board), np.copy(chess_y_board), np.copy(chess_name)
    if not on_cross(srcx, srcy):
        print('Quân cờ không đặt trên các đường giao')
        return None
    size = len(srcname)
    state = [['.' for _ in range(9)] for _ in range(10)]
    for i in range(size):
        x, y = 9 - round((srcy[i] - 20) / 41), round((srcx[i] - 20) / 41)
        state[x][y] = chess_eng[srcname[i]]
    state = np.array(state)
    if not valid_position(state):
        print('Lỗi: Trạng thái không hợp lệ')
        return None
    return matrix2fen(state)