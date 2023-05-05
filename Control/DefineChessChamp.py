import numpy as np

from Network.Network import *

client_recognize = Client(8082)


def define_chess_champ():
    data_send = ['Go']
    client_recognize.send(data_send)
    while True:
        data_receive = client_recognize.receive()
        if data_receive[0] == 'Done':
            break
    data = np.loadtxt('D:\\chinese-chess-robot\\Camera\\data.csv', delimiter=',', dtype=int)
    chess_x_board = data[:, 0]
    chess_y_board = data[:, 1]
    chess_int = data[:, 2]
    return chess_x_board, chess_y_board, chess_int


# data = np.loadtxt('D:\\chinese-chess-robot\\Camera\\data.csv', delimiter=',', dtype=int)
# chess_x_board = data[:, 0]
# chess_y_board = data[:, 1]
# chess_int = data[:, 2]
# srcx, srcy, srcname = np.copy(chess_x_board), np.copy(chess_y_board), np.copy(chess_int)
# print(len(srcx))
