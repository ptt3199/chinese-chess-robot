# call API chessdb
from ValidateState import *
from Utils.VisionUtils import *
from PLCControl.PLCControl import *
from Const.VisionConst import *

url = 'https://www.chessdb.cn/chessdb.php?action=querybest&board='
original_fen = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
previous_state = fen2matrix(original_fen)


def explain_move(mov):
    src_x = ord(mov[0]) - ord('a') + 1
    dst_x = ord(mov[2]) - ord('a') + 1
    src_y = mov[1]
    dst_y = mov[3]
    return src_x, src_y, dst_x, dst_y


def play_chess(chess_x_image, chess_y_image, chess_int):
    if wrong_position(chess_x_image, chess_y_image):
        print('Quân cờ không đặt trên các đường giao')
        return None

    state, real_loc_x, real_loc_y = get_board(chess_x_image, chess_y_image, chess_int)

    src_x, src_y, dst_x, dst_y = define_move(previous_state, state)
    if src_x == '':
        print('Ít hoặc nhiều hơn một nước đi')

    # request
    mov = previous_moves + src_x + str(src_y) + dst_x + str(dst_y)

    # receive
    receiver = requests.get(url + original_fen + '_w' + '_moves_' + mov, stream=True)
    mov = receiver.text[5:9]
    if mov == 'invalid board':
        print('Trạng thái bàn cờ không hợp lệ: Thiếu - thừa quân hoặc quân không đúng vị trí cho phép')
        return None
    src_x, src_y, dst_x, dst_y = explain_move(mov)
    x1, x2 = real_loc_x[src_y], dst_y * 41 + 20
    y1, y2 = real_loc_y[src_x], (9 - dst_x) * 41 + 20
    print('Computer move: ', state[src_x][src_y], (src_x, src_y), '->', (dst_x, dst_y))
    if state[dst_x][dst_y] == '.':
        print('Move from ', (x1, y1), 'to', (x2, y2))
        move(x1, y1, x2, y2)
    else:
        print('Capture from ', (x1, y1), 'to', (x2, y2))
        capture(x1, y1, x2, y2)

    previous_state[:, :] = state[:, :]
    # save new state
    state[dst_x][dst_y] = state[src_x][src_y]
    state[src_x][src_y] = '.'

    # print state
    fen2matrix_cn(fen_receive, mov)
    print('Your turn!')
