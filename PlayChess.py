from Const.VisionConst import *
from PLCControl.PLCControl import *
from Utils.VisionUtils import *
from Network.Network import *

"""==================== Login to chess engine server ===================="""
client_engine = Client(8080)
ply = 5


def wrong_position(chess_x_image, chess_y_image):  # error 1
    x_rights = [20, 61, 102, 143, 184, 225, 266, 307, 348]
    y_rights = [20, 61, 102, 143, 184, 225, 266, 307, 348, 389]
    error = 6
    x_fail, y_fail = False, False
    size = len(chess_x_image)
    for i in range(size):
        for x in range(7):
            if x_rights[x] + error <= chess_x_image[i] <= x_rights[x + 1] - error:
                x_fail = True
        for y in range(8):
            if y_rights[y] + error <= chess_y_image[i] <= y_rights[y + 1] - error:
                y_fail = True
    return x_fail and y_fail


def check_king_opposite(state, i, j, lowercase=True):
    if lowercase:
        for k in range(i + 1, 10):
            if state[k][j] == 'K':
                return True
            elif state[k][j] != '.' or k == 9:
                return False
    else:
        for k in range(i - 1, -1, -1):
            if state[k][j] == 'K':
                return True
            elif state[k][j] != '.' or k == 0:
                return False


def validate_state(state):
    COLUMN, ROW = 9, 10
    k_pos = 0  # black king position =0 have not appeared King,=1 Black on Top,=2 Black on Bottom
    a_pos = 0  # black advisor position =0 have not appeared Avisor,=1 Black on Top,=2 Black on Bottom
    e_pos = 0  # black elephant position =0 have not appeared Elephant,=1 Black on Top,=2 Black on Bottom
    # ck = count + k = count black king; cK = count + K = count red King
    cK, ca, cA, ce, cE, cr, cR, cc, cC, ch, cH, cp, cP = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for i in range(ROW):
        for j in range(COLUMN):
            if state[i][j] == 'r':
                if cr == 2:
                    return False
                else:
                    cr += 1
            elif state[i][j] == 'R':
                if cR == 2:
                    return False
                else:
                    cR += 1
            elif state[i][j] == 'c':
                if cc == 2:
                    return False
                else:
                    cc += 1
            elif state[i][j] == 'C':
                if cC == 2:
                    return False
                else:
                    cC += 1
            elif state[i][j] == 'h':
                if ch == 2:
                    return False
                else:
                    ch += 1
            elif state[i][j] == 'H':
                if cH == 2:
                    return False
                else:
                    cH += 1
            elif state[i][j] == 'k':
                if cK == 2:
                    return False
                else:
                    cK += 1
                if i < 3:
                    if a_pos == 2 or e_pos == 2 or k_pos == 2:
                        return False
                    k_pos = 1  # black king on Top of Board
                    if j < 3 or j > 5:
                        return False
                    elif check_king_opposite(state, i, j, True):
                        return False
                elif i > 6:
                    if a_pos == 1 or e_pos == 1 or k_pos == 1:
                        return False
                    k_pos = 2
                    if j < 3 or j > 5:
                        return False
                    elif Validator.check_king_opposite(state, i, j, False):
                        return False
                else:
                    return False
            elif state[i][j] == 'K':
                if cK == 2:
                    return False
                else:
                    cK += 1
                if i < 3:
                    if a_pos == 1 or e_pos == 1 or k_pos == 1:
                        return False
                    k_pos = 2
                    if j < 3 or j > 5:
                        return False
                elif i > 6:
                    if a_pos == 2 or e_pos == 2 or k_pos == 2:
                        return False
                    k_pos = 1
                    if j < 3 or j > 5:
                        return False
                else:
                    return False
            elif state[i][j] == 'a':
                if ca == 2:
                    return False
                else:
                    ca += 1
                if i < 3:
                    if k_pos == 2:
                        return False
                    a_pos = 1
                    if i > 2 or (i == 1 and j != 4) or (i == 2 and j == 4) or j < 3 or j > 5 or (i == 0 and j == 4):
                        return False
                else:
                    if k_pos == 1:
                        return False
                    a_pos = 2
                    if i < 7 or (i == 8 and j != 4) or (i == 7 and j == 4) or j < 3 or j > 5 or (i == 9 and j == 4):
                        return False
            elif state[i][j] == 'A':
                if cA == 2:
                    return False
                else:
                    cA += 1
                if i < 3:
                    if k_pos == 1:
                        return False
                    a_pos = 2
                    if i > 2 or (i == 1 and j != 4) or (i == 2 and j == 4) or j < 3 or j > 5 or (i == 0 and j == 4):
                        return False
                else:
                    if k_pos == 2:
                        return False
                    a_pos = 1
                    if i < 7 or (i == 8 and j != 4) or (i == 7 and j == 4) or j < 3 or j > 5 or (i == 9 and j == 4):
                        return False
            elif state[i][j] == 'e':
                if ce == 2:
                    return False
                else:
                    ce += 1
                if i < 5:
                    if k_pos == 2:
                        return False
                    if i == 1 or i == 3:
                        return False
                    elif (i == 0 or i == 4) and j != 2 and j != 6:
                        return False
                    elif i == 2 and j != 0 and j != 4 and j != 8:
                        return False
                    e_pos = 1
                elif i > 4:
                    if k_pos == 1:
                        return False
                    elif i == 8 or i == 6:
                        return False
                    elif (i == 9 or i == 5) and j != 2 and j != 6:
                        return False
                    elif i == 7 and j != 0 and j != 4 and j != 8:
                        return False
                    e_pos = 2
            elif state[i][j] == 'E':
                if cE == 2:
                    return False
                else:
                    cE += 1
                if i < 5:
                    if k_pos == 1:
                        return False
                    if i == 1 or i == 3:
                        return False
                    elif (i == 0 or i == 4) and j != 2 and j != 6:
                        return False
                    elif i == 2 and j != 0 and j != 4 and j != 8:
                        return False
                    e_pos = 2
                elif i > 4:
                    if k_pos == 2:
                        return False
                    elif i == 8 or i == 6:
                        return False
                    elif (i == 9 or i == 5) and j != 2 and j != 6:
                        print(111)
                        return False
                    elif i == 7 and j != 0 and j != 4 and j != 8:
                        return False
                    e_pos = 1
            elif k_pos == 1:  # King Black on top Board
                if state[i][j] == 'p':
                    cp += 1
                    if i < 3:
                        return False
                    elif 3 <= i < 5 and (j == 1 or j == 3 or j == 5 or j == 7):
                        return False
                elif state[i][j] == 'P':
                    cP += 1
                    if i > 6:
                        return False
                    elif 6 >= i > 4 and (j == 1 or j == 3 or j == 5 or j == 7):
                        return False
            elif k_pos == 2:
                if state[i][j] == 'P':
                    cP += 1
                    if i < 3:
                        return False
                    elif 3 <= i < 5 and (j == 1 or j == 3 or j == 5 or j == 7):
                        return False
                elif state[i][j] == 'p':
                    cp += 1
                    if i > 6:
                        return False
                    elif 6 >= i > 4 and (j == 1 or j == 3 or j == 5 or j == 7):
                        return False
    if cK < 2:
        print(1111)
        return False
    else:
        return True


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
        print('Quân cờ đặt sai vị trí')
        return None

    board, real_loc_x, real_loc_y = get_board(chess_x_image, chess_y_image, chess_int)
    fen_send = matrix2fen(board)
    data = [fen_send + ' w', ply]
    client_engine.send(data)
    [fen_receive, mov] = client_engine.receive()
    src_x, src_y, dst_x, dst_y = move_in_state(mov)
    # x1, x2 = src_y * 41 + 20, dst_y * 41 + 20
    x1, x2 = real_loc_x[src_y], dst_y * 41 + 20
    # y1, y2 = (9 - src_x) * 41 + 20, (9 - dst_x) * 41 + 20
    y1, y2 = real_loc_y[src_x], (9 - dst_x) * 41 + 20
    print('Computer move: ', board[src_x][src_y], (src_x, src_y), '->', (dst_x, dst_y))
    if board[dst_x][dst_y] == '.':
        print('Move from ', (x1, y1), 'to', (x2, y2))
        move(x1, y1, x2, y2)
    else:
        print('Capture from ', (x1, y1), 'to', (x2, y2))
        capture(x1, y1, x2, y2)
    board[dst_x][dst_y] = board[src_x][src_y]
    board[src_x][src_y] = '.'
    fen2matrix_cn(fen_receive, mov)
    print('Your turn!')
