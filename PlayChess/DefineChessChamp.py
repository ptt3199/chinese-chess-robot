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
    chess_x = data[:, 0]
    chess_y = data[:, 1]
    chess_int = (data[:, 2]).astype(int)

    return chess_x, chess_y, chess_int
