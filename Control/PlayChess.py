from playsound import playsound

from Const.VisionConst import *
from PLCControl.PLCControl import *
from Utils.VisionUtils import *
from Network.Network import *
from Control.ValidateState import *

# for debugging
# from Control.DefineChessChamp import *

"""==================== Login to chess engine server ===================="""
client_engine = Client(8080)


def get_state(chess_x_board, chess_y_board, chess_name):
    print('Get state:....')
    srcx, srcy, srcname = np.copy(chess_x_board), np.copy(chess_y_board), np.copy(chess_name)
    if not on_cross(srcx, srcy):
        print('Quân cờ không đặt trên các đường giao')
        playsound('Sound\\bancosai.wav')
        return None, None, None

    size = len(srcname)
    state = [['.' for _ in range(9)] for _ in range(10)]
    real_loc_x, real_loc_y = [[0 for _ in range(9)] for _ in range(10)], [[0 for _ in range(9)] for _ in range(10)]
    for i in range(size):
        x, y = 9 - round((srcy[i] - 20) / 41), round((srcx[i] - 20) / 41)
        state[x][y] = chess_eng[srcname[i]]
        real_loc_x[x][y] = srcy[i]
        real_loc_y[x][y] = srcx[i]
    return np.array(state), real_loc_x, real_loc_y


def play_chess(previous_fen, chess_x_board, chess_y_board, chess_name, level=2):
    state, real_loc_x, real_loc_y = get_state(chess_x_board, chess_y_board, chess_name)
    previous_state = fen2matrix(previous_fen)
    if state is None or not valid_move(previous_state, state):
        print('Nước đi không hợp lệ')
        print('===============================')
        playsound('Sound\\nuocdisai.wav')

        opc.write(('Channel2.Device1.Y11', 1))  # bật đèn đỏ báo nước đi sai

        return previous_fen

    opc.write(('Channel2.Device1.Y11', 0))  # tắt đèn báo nước đi sai nếu nó đang bật

    print('Trạng thái hiện tại:', matrix2fen(state))
    print(state)

    fen_send = matrix2fen(state)
    ply = 3  # gía trị mặc định
    if level == 1:
        ply = 3
    elif level == 2:
        ply = 4
    elif level == 3:
        ply = 5
    data = [fen_send + ' w', ply]
    client_engine.send(data)

    [fen_receive, mov] = client_engine.receive()
    src_x, src_y, dst_x, dst_y = move_in_state(mov)
    print('Nước đi của máy: ', state[src_x][src_y], (src_x, src_y), '->', (dst_x, dst_y))

    playsound('Sound\\luotcuarobot.wav')
    x1, y1 = real_loc_y[src_x][src_y], real_loc_x[src_x][src_y]
    if state[dst_x][dst_y] == '.':
        x2, y2 = dst_y * 41 + 20, (9 - dst_x) * 41 + 20
        print('Move from ', (x1, y1), 'to', (x2, y2))
        move(x1, y1, x2, y2)
    else:
        x2, y2 = real_loc_y[dst_x][dst_y], real_loc_x[dst_x][dst_y]
        print('Capture from ', (x1, y1), 'to', (x2, y2))
        capture(x1, y1, x2, y2)
    opc.write(('Channel2.Device1.Y7', 1))  # bật đèn lượt người chơi

    state[dst_x][dst_y] = state[src_x][src_y]
    state[src_x][src_y] = '.'
    print('Trạng thái mới: ', fen_receive)
    fen2matrix_cn(fen_receive, mov)
    print('Lượt người chơi!')
    print('=====================================')
    playsound('Sound\\luotcuaban.wav')

    return matrix2fen(state)


def play_chess_1_time_robot_first(previous_fen, chess_x_board, chess_y_board, chess_name, level=2):
    state, real_loc_x, real_loc_y = get_state(chess_x_board, chess_y_board, chess_name)
    if state is None:
        print('Trạng thái bàn cờ không hợp lệ')
        print('===============================')
        playsound('Sound\\nuocdisai.wav')

        opc.write(('Channel2.Device1.Y11', 1))  # bật đèn đỏ báo nước đi sai

        return previous_fen

    opc.write(('Channel2.Device1.Y11', 0))  # tắt đèn báo nước đi sai nếu nó đang bật

    print('Trạng thái hiện tại:', matrix2fen(state))
    print(state)

    fen_send = matrix2fen(state)
    ply = 5  # gía trị mặc định
    if level == 1:
        ply = 3
    elif level == 2:
        ply = 4
    elif level == 3:
        ply = 5
    data = [fen_send + ' w', ply]
    client_engine.send(data)
    [fen_receive, mov] = client_engine.receive()
    src_x, src_y, dst_x, dst_y = move_in_state(mov)
    print('Nước đi của máy: ', state[src_x][src_y], (src_x, src_y), '->', (dst_x, dst_y))

    playsound('Sound\\luotcuarobot.wav')
    x1, y1 = real_loc_y[src_x][src_y], real_loc_x[src_x][src_y]
    if state[dst_x][dst_y] == '.':
        x2, y2 = dst_y * 41 + 20, (9 - dst_x) * 41 + 20
        print('Move from ', (x1, y1), 'to', (x2, y2))
        move(x1, y1, x2, y2)
    else:
        x2, y2 = real_loc_y[dst_x][dst_y], real_loc_x[dst_x][dst_y]
        print('Capture from ', (x1, y1), 'to', (x2, y2))
        capture(x1, y1, x2, y2)

    opc.write(('Channel2.Device1.Y7', 1))  # bật đèn lượt người chơi

    for idi in range(0, 2):
        for idj in range(3, 6):
            if state[idi, idj] == 'k':
                if not king_is_not_checked(state, idi, idj):
                    playsound('Sound\\chieutuong.wav')
                    break

    state[dst_x][dst_y] = state[src_x][src_y]
    state[src_x][src_y] = '.'
    print('Trạng thái mới: ', fen_receive)
    fen2matrix_cn(fen_receive, mov)

    print('Lượt người chơi!')
    print('=====================================')
    playsound('Sound\\luotcuaban.wav')

    return matrix2fen(state)


# for debugging
# cx, cy, cname = define_chess_champ()
# previous_fen = '2ea5/3Ra4/3c1k3/p1p6/5HP2/9/P3H4/5C3/1C3K3/2EA4r'
# previous_fen = play_chess(previous_fen, cx, cy, cname, 3)
