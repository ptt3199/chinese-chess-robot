from Const.VisionConst import *
from PLCControl.PLCControl import *
from Utils.VisionUtils import *
from Network.Network import *
from ValidateState import *

"""==================== Login to chess engine server ===================="""
client_engine = Client(8080)
ply = 5
previous_state = ''


def get_board(chess_x_image, chess_y_image, chess_int):
    size = len(chess_int)
    # board = []
    state = [['.' for _ in range(9)] for _ in range(10)]
    real_loc_x, real_loc_y = [[0 for _ in range(9)] for _ in range(10)]
    # for i in range(10):
    #     row = []
    #     for j in range(9):
    #         row.append(".")
    #     board.append(row)
    for i in range(size):
        x = round((chess_x_image[i] - margin_image) / chess_piece_size_image)
        y = round((chess_y_image[i] - margin_image) / chess_piece_size_image)
        state[y][x] = chess_eng[chess_int[i]]
        real_loc_x[y][x] = chess_x_image[i]
        real_loc_y[y][x] = chess_y_image[i]
    return state, real_loc_x, real_loc_y


def play_chess(chess_x_image, chess_y_image, chess_int):
    if wrong_position(chess_x_image, chess_y_image):
        print('Quân cờ không đặt trên các đường giao')
        return None

    state, real_loc_x, real_loc_y = get_board(chess_x_image, chess_y_image, chess_int)
    if not valid_state(state):
        print('Trạng thái bàn cờ không hợp lệ: Thiếu - thừa quân hoặc quân không đúng vị trí cho phép')
        return None
    src_x, src_y, dst_x, dst_y = define_move(previous_state, state)
    if src_x == '':
        print('Ít hoặc nhiều hơn một nước đi')
    fen_send = matrix2fen(state)
    data = [fen_send + ' w', ply]
    client_engine.send(data)

    [fen_receive, mov] = client_engine.receive()
    src_x, src_y, dst_x, dst_y = move_in_state(mov)
    # x1, x2 = src_y * 41 + 20, dst_y * 41 + 20
    x1, x2 = real_loc_x[src_y], dst_y * 41 + 20
    # y1, y2 = (9 - src_x) * 41 + 20, (9 - dst_x) * 41 + 20
    y1, y2 = real_loc_y[src_x], (9 - dst_x) * 41 + 20
    print('Computer move: ', state[src_x][src_y], (src_x, src_y), '->', (dst_x, dst_y))
    if state[dst_x][dst_y] == '.':
        print('Move from ', (x1, y1), 'to', (x2, y2))
        move(x1, y1, x2, y2)
    else:
        print('Capture from ', (x1, y1), 'to', (x2, y2))
        capture(x1, y1, x2, y2)
    state[dst_x][dst_y] = state[src_x][src_y]
    state[src_x][src_y] = '.'
    fen2matrix_cn(fen_receive, mov)
    print('Your turn!')
