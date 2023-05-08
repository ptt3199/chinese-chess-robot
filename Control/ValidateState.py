
def on_cross(chess_x_image, chess_y_image):  # kiểm tra quân cờ có nằm trên đường giao không
    x_lines = [20, 61, 102, 143, 184, 225, 266, 307, 348]
    y_lines = [20, 61, 102, 143, 184, 225, 266, 307, 348, 389]
    error = 10
    x_ok, y_ok = True, True
    size = len(chess_x_image)
    for i in range(size):
        for x in range(8):  # nằm giữa 2 đường x
            if x_lines[x] + error <= chess_x_image[i] <= x_lines[x + 1] - error:
                x_ok = False
        for y in range(9):  # nằm giữa 2 đường y
            if y_lines[y] + error <= chess_y_image[i] <= y_lines[y + 1] - error:
                y_ok = False
    return x_ok and y_ok


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


def valid_position(state):  # kiểm tra quân cờ có đúng số lượng, nằm trong phạm vi cho phép không
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
                    print('Lỗi: Dư xe đen')
                    return False
                else:
                    cr += 1
            elif state[i][j] == 'R':
                if cR == 2:
                    print('Lỗi: Dư xe đỏ')
                    return False
                else:
                    cR += 1
            elif state[i][j] == 'c':
                if cc == 2:
                    print('Lỗi: Dư pháo đen')
                    return False
                else:
                    cc += 1
            elif state[i][j] == 'C':
                if cC == 2:
                    print('Lỗi: Dư pháo đỏ')
                    return False
                else:
                    cC += 1
            elif state[i][j] == 'h':
                if ch == 2:
                    print('Lỗi: Dư mã đen')
                    return False
                else:
                    ch += 1
            elif state[i][j] == 'H':
                if cH == 2:
                    print('Lỗi: Dư mã đỏ')
                    return False
                else:
                    cH += 1
            elif state[i][j] == 'k':
                if cK == 2:
                    print('Lỗi: Dư tướng')
                    return False
                else:
                    cK += 1
                if i < 3:
                    if a_pos == 2 or e_pos == 2 or k_pos == 2:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng không ở đúng phía')
                        return False
                    k_pos = 1  # black king on Top of Board
                    if j < 3 or j > 5:
                        return False
                    elif check_king_opposite(state, i, j, True):
                        print('Lỗi vị trí: Lộ mặt tướng')
                        return False
                elif i > 6:
                    if a_pos == 1 or e_pos == 1 or k_pos == 1:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng không ở đúng phía')
                        return False
                    k_pos = 2
                    if j < 3 or j > 5:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng ra khỏi cung')
                        return False
                    elif check_king_opposite(state, i, j, False):
                        print('Lỗi vị trí: Lộ mặt tướng')
                        return False
                else:
                    print('Lỗi vị trí: Sĩ, Tượng, Tướng ra khỏi cung')
                    return False
            elif state[i][j] == 'K':
                if cK == 2:
                    print('Lỗi: Dư tướng')
                    return False
                else:
                    cK += 1
                if i < 3:
                    if a_pos == 1 or e_pos == 1 or k_pos == 1:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng không ở đúng phía')
                        return False
                    k_pos = 2
                    if j < 3 or j > 5:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng ra khỏi cung')
                        return False
                elif i > 6:
                    if a_pos == 2 or e_pos == 2 or k_pos == 2:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng không ở đúng phía')
                        return False
                    k_pos = 1
                    if j < 3 or j > 5:
                        print('Lỗi vị trí: Sĩ, Tượng, Tướng ra khỏi cung')
                        return False
                else:
                    print('Lỗi vị trí: Sĩ, Tượng, Tướng ra khỏi cung')
                    return False
            elif state[i][j] == 'a':
                if ca == 2:
                    print('Lỗi: Dư sĩ đen')
                    return False
                else:
                    ca += 1
                if i < 3:
                    if k_pos == 2:
                        print('Lỗi vị trí: Sĩ không ở đúng phía')
                        return False
                    a_pos = 1
                    if i > 2 or (i == 1 and j != 4) or (i == 2 and j == 4) or j < 3 or j > 5 or (i == 0 and j == 4):
                        print('Lỗi vị trí: Sĩ không ở trong cung')
                        return False
                else:
                    if k_pos == 1:
                        print('Lỗi vị trí: Sĩ không ở đúng phía')
                        return False
                    a_pos = 2
                    if i < 7 or (i == 8 and j != 4) or (i == 7 and j == 4) or j < 3 or j > 5 or (i == 9 and j == 4):
                        print('Lỗi vị trí: Sĩ không ở trong cung')
                        return False
            elif state[i][j] == 'A':
                if cA == 2:
                    print('Lỗi: Dư sĩ đỏ')
                    return False
                else:
                    cA += 1
                if i < 3:
                    if k_pos == 1:
                        print('Lỗi vị trí: Sĩ không ở đúng phía')
                        return False
                    a_pos = 2
                    if i > 2 or (i == 1 and j != 4) or (i == 2 and j == 4) or j < 3 or j > 5 or (i == 0 and j == 4):
                        print('Lỗi vị trí: Sĩ không ở trong cung')
                        return False
                else:
                    if k_pos == 2:
                        print('Lỗi vị trí: Sĩ không ở đúng phía')
                        return False
                    a_pos = 1
                    if i < 7 or (i == 8 and j != 4) or (i == 7 and j == 4) or j < 3 or j > 5 or (i == 9 and j == 4):
                        print('Lỗi vị trí: Sĩ không ở trong cung')
                        return False
            elif state[i][j] == 'e':
                if ce == 2:
                    print('Lỗi: Dư tượng đen')
                    return False
                else:
                    ce += 1
                if i < 5:
                    if k_pos == 2:
                        print('Lỗi vị trí: Tượng không ở đúng phía')
                        return False
                    if i == 1 or i == 3:
                        print('Lỗi vị trí: Tượng không ở đúng vị trí đi được')
                        return False
                    elif (i == 0 or i == 4) and j != 2 and j != 6:
                        print('Lỗi vị trí: Tượng không ở đúng vị trí đi được')
                        return False
                    elif i == 2 and j != 0 and j != 4 and j != 8:
                        print('Lỗi vị trí: Tượng không ở đúng vị trí đi được')
                        return False
                    e_pos = 1
                elif i > 4:
                    if k_pos == 1:
                        print('Lỗi vị trí: Tượng không ở đúng phía')
                        return False
                    elif i == 8 or i == 6:
                        print('Lỗi vị trí: Tượng không ở đúng vị trí đi được')
                        return False
                    elif (i == 9 or i == 5) and j != 2 and j != 6:
                        print('Lỗi vị trí: Tượng không ở đúng vị trí đi được')
                        return False
                    elif i == 7 and j != 0 and j != 4 and j != 8:
                        print('Lỗi vị trí: Tượng không ở đúng vị trí đi được')
                        return False
                    e_pos = 2
            elif state[i][j] == 'E':
                if cE == 2:
                    print('Lỗi: Dư tượng đỏ')
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


def king_is_not_check(st, di, dj):
    # 1. Chiếu bởi tốt đỏ: tốt bên dưới, bên trái, bên phải
    if st[di + 1][dj] == 'P' or st[di][dj - 1] == 'P' or st[di][dj + 1] == 'P':
        print('Lỗi: Đi vào ô bị chiếu bởi tốt')
        return False

    # 2. Chiếu bởi mã đỏ (không viết logic phức tạp để tiện debug)
    # 2 điểm i - 2
    if di - 2 >= 0 and st[di - 1][dj] == '.' and (st[di - 2][dj - 1] == 'H' or st[di - 2][dj + 1] == 'H'):
        print('Lỗi: Đi vào ô bị chiếu bởi mã')
        return False
    # 2 điểm i - 1
    if di - 1 >= 0:
        if st[di][dj - 1] == '.' and st[di - 1][dj - 2] == 'H':
            print('Lỗi: Đi vào ô bị chiếu bởi mã')
            return False
        if st[di][dj + 1] == '.' and st[di - 1][dj + 2] == 'H':
            print('Lỗi: Đi vào ô bị chiếu bởi mã')
            return False
    # 2 điểm i + 1
    if st[di][dj - 1] == '.' and st[di + 1][dj - 2] == 'H':
        print('Lỗi: Đi vào ô bị chiếu bởi mã')
        return False
    if st[di][dj + 1] == '.' and st[di + 1][dj + 2] == 'H':
        print('Lỗi: Đi vào ô bị chiếu bởi mã')
        return False
    # 2 điểm i + 2
    if st[di + 1][dj] == '.' and (st[di + 2][dj - 1] == 'H' or st[di + 2][dj + 1] == 'H'):
        print('Lỗi: Đi vào ô bị chiếu bởi mã')
        return False

    # 3. Chiếu bởi xe đỏ
    # Dò trục ngang
    idj = dj - 1
    while idj >= 0:
        if st[di][idj] == 'R':
            print('Lỗi: Đi vào ô bị chiếu bởi xe')
            return False
        if st[di][idj] == '.':
            idj = idj - 1
        else:
            break

    idj = dj + 1
    while idj <= 8:
        if st[di][idj] == 'R':
            print('Lỗi: Đi vào ô bị chiếu bởi xe')
            return False
        if st[di][idj] == '.':
            idj = idj + 1
        else:
            break

    # Dò trục dọc
    idi = di - 1
    while idi >= 0:
        if st[idi][dj] == 'R':
            print('Lỗi: Đi vào ô bị chiếu bởi xe')
            return False
        if st[idi][dj] == '.':
            idi = idi - 1
        else:
            break

    idi = di + 1
    while idi <= 9:
        if st[idi][dj] == 'R':
            print('Lỗi: Đi vào ô bị chiếu bởi xe')
            return False
        if st[idi][dj] == '.':
            idi = idi + 1
        else:
            break

    # 4. Chiếu bởi pháo đỏ
    # Dò trục ngang
    idj = dj - 1
    count_champ = 0  # đếm số quân cờ trước khi gặp quân pháo
    while idj >= 0:
        if st[di][idj] == 'C' and count_champ == 1:
            print('Lỗi: Tướng bị chiếu bởi pháo')
            return False
        if st[di][idj] != '.':
            count_champ += 1
        if count_champ > 1:
            break
        idj = idj - 1

    idj = dj + 1
    count_champ = 0  # đếm số quân cờ trước khi gặp quân pháo
    while idj <= 8:
        if st[di][idj] == 'C' and count_champ == 1:
            print('Lỗi: Tướng bị chiếu bởi pháo')
            return False
        if st[di][idj] != '.':
            count_champ += 1
        if count_champ > 1:
            break
        idj = idj + 1

    # Dò trục dọc
    idi = di - 1
    count_champ = 0  # đếm số quân cờ trước khi gặp quân pháo
    while idi >= 0:
        if st[idi][dj] == 'C' and count_champ == 1:
            print('Lỗi: Tướng bị chiếu bởi pháo')
            return False
        if st[idi][dj] != '.':
            count_champ += 1
        if count_champ > 1:
            break
        idi = idi - 1

    idi = di + 1
    count_champ = 0  # đếm số quân cờ trước khi gặp quân pháo
    while idi <= 9:
        if st[idi][dj] == 'C' and count_champ == 1:
            print('Lỗi: Đi vào ô bị chiếu bởi pháo')
            return False
        if st[idi][dj] != '.':
            count_champ += 1
        if count_champ > 1:
            break
        idi = idi + 1
    return True


def valid_move_rook(st, si, sj, di, dj):  # ok
    # Nếu không ở vị trí thẳng hàng theo bất kì trục nào thì False
    if si != di and sj != dj:
        return False
    # Nếu ở bên cạnh
    if (abs(si - di) == 1 and sj == dj) or (abs(sj - dj) == 1 and si == di):
        return True
    # Chạy dọc theo từng trục, nếu có quân cờ cản đường thì trả về False
    if si == di:  # di ngang
        if sj < dj:
            for idj in range(sj + 1, dj):
                if st[si, idj] != '.':
                    return False
        else:
            for idj in range(dj + 1, sj):
                if st[si, idj] != '.':
                    return False
    elif sj == dj:
        if si < di:
            for idi in range(si + 1, di):
                if st[idi, sj] != '.':
                    return False
        else:
            for idi in range(di + 1, si):
                if st[idi, sj] != '.':
                    return False
    return True


def valid_move_horse(st, si, sj, di, dj):  # ok
    # Nếu không ở đúng vị trí so với nhau
    if (abs(si - di) == 2 and abs(sj - dj) != 1) or (abs(si - di) == 1 and abs(sj - dj) != 2):
        return False
    # Nếu bị chặn
    if (si - 2 == di and st[si - 1][sj] != '.') \
            or (si + 2 == di and st[si + 1][sj] != '.') \
            or (sj - 2 == dj and st[si][sj - 1] != '.') \
            or (sj + 2 == dj and st[si][sj + 1] != '.'):
        return False
    return True


def valid_move_elephant(st, si, sj, di, dj):  # ok
    if abs(si - di) != 2 or abs(sj - dj) != 2:
        return False
    if st[(si + di) // 2][(sj + dj) // 2] != '.':
        return False
    return True


# noinspection PyUnusedLocal
def valid_move_advisor(st, si, sj, di, dj):  # ok
    if abs(si - di) != 1 or abs(sj - dj) != 1:
        return False
    return True


# noinspection PyUnusedLocal
def valid_move_pawn(st, si, sj, di, dj):
    # chỉ xét quân đen (quân của người chơi)
    if (si + 1 == di and sj == dj) or ((si == di) and (si > 4) and abs(sj - dj) == 1):
        return True
    else:
        print('Lỗi: Tốt đi sai')


def valid_move_cannon(st, si, sj, di, dj):  # ok
    # Nếu đi quân: điểm đến trống
    if st[di, dj] == '.':
        return valid_move_rook(st, si, sj, di, dj)
    # Nếu là ăn quân
    # # Nếu cạnh nhau là sai
    # if (abs(si - di) == 1 and sj == dj) or (abs(sj - dj) == 1 and si == di):
    #     return False
    # Chạy dọc theo từng trục, nếu có != 1 quân cờ cản đường thì trả về False
    count_block = 0
    if si == di:  # di ngang
        for idj in range(sj + 1, dj):
            if st[si, idj] != '.':
                count_block += 1
    elif sj == dj:  # đi dọc
        for idi in range(si + 1, di):
            if st[idi, sj] != '.':
                count_block += 1
    return count_block == 1


def valid_move_king(st, si, sj, di, dj):
    # Nếu không thẳng hàng thì sai
    if si != di and sj != dj:
        print('Lỗi: Tướng không đi đường thẳng')
        return False
    # Nếu đi khác 1 bước
    if (abs(si - di) != 1 and sj == dj) or (abs(sj - dj) != 1 and si == di):
        print('Lỗi: Tướng đi nhiều hơn 1 bước')
        return False
    # Nếu lộ mặt tướng -> đã xét ở valid_position
    # Nếu đi vào ô bị chiếu
    if king_is_not_check(st, di, dj):
        return False
    return True


def valid_move(previous_state, state):
    print('Define and check valid move:...')
    if not valid_position(state):
        print('Trạng thái bàn cờ không hợp lệ: Thừa quân hoặc quân không đúng vị trí cho phép')
        return False

    champ_name = ''
    found_src, found_dst = 0, 0
    src_i, src_j, dst_i, dst_j = -1, -1, -1, -1
    for i in range(10):
        for j in range(9):
            if previous_state[i][j] != '.' and state[i][j] == '.':
                src_i, src_j = i, j
                champ_name = previous_state[i][j]  # tên quân cờ
                found_src += 1
                if found_src > 1:
                    print('Nhiều hơn 1 nước đi')
                    return False
            elif (previous_state[i][j] != '.' and previous_state[i][j] != state[i][j]) or (
                    previous_state[i][j] == '.' and state[i][j] != '.'):
                dst_i, dst_j = i, j
                found_dst += 1
                if found_dst > 1:
                    print('Nhiều hơn 1 nước đi')
                    return False
    if champ_name == '':
        return False
    # Nếu ăn quân cùng phe
    black = ['a', 'c', 'e', 'h', 'k', 'p', 'r']
    red = ['A', 'C', 'E', 'H', 'K', 'P']
    if (previous_state[dst_i][dst_j] in black and state[dst_i][dst_j] in black) \
            or (previous_state[dst_i][dst_j] in red and state[dst_i][dst_j] in red)\
            or (dst_i == -1 and dst_j == -1):
        print('Ăn quân cùng phe')
        return False

    # Nếu khiến tướng bị chiếu
    for idi in range(0, 2):
        for idj in range(3, 6):
            if state[idi, idj] == 'k':
                if king_is_not_check(state, idi, idj):
                    break
                else:
                    print('Lỗi: Nước đi khiến Tướng bị chiếu')
                    return False
    print('Người đi: ', champ_name, (src_i, src_j), '->', (dst_i, dst_j))
    if champ_name.capitalize() == 'R':
        return valid_move_rook(previous_state, src_i, src_j, dst_i, dst_j)
    if champ_name.capitalize() == 'H':
        return valid_move_horse(previous_state, src_i, src_j, dst_i, dst_j)
    if champ_name.capitalize() == 'E':
        return valid_move_elephant(previous_state, src_i, src_j, dst_i, dst_j)
    if champ_name.capitalize() == 'A':
        return valid_move_advisor(previous_state, src_i, src_j, dst_i, dst_j)
    if champ_name.capitalize() == 'K':
        return valid_move_king(previous_state, src_i, src_j, dst_i, dst_j)
    if champ_name.capitalize() == 'C':
        return valid_move_cannon(previous_state, src_i, src_j, dst_i, dst_j)
    if champ_name.capitalize() == 'P':
        return valid_move_pawn(previous_state, src_i, src_j, dst_i, dst_j)
    return False


#  for debugging
from Utils.VisionUtils import *
pfen = 'r1e1ka3/1R2a4/4c3e/p1p1C3p/9/9/P1H1H1p1P/7C1/9/2EAKAE2'
pst = fen2matrix(pfen)
fen = 'r1ek1a3/1R2a4/4c3e/p1p1C3p/9/9/P1H1H1p1P/7C1/9/2EAKAE2'
st = fen2matrix(fen)
valid_move(pst, st)
