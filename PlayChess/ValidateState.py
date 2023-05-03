def on_cross(chess_x_image, chess_y_image):  # kiểm tra quân cờ có nằm trên đường giao không
    x_rights = [20, 61, 102, 143, 184, 225, 266, 307, 348]
    y_rights = [20, 61, 102, 143, 184, 225, 266, 307, 348, 389]
    error = 6
    x_fail, y_fail = False, False
    size = len(chess_x_image)
    for i in range(size):
        for x in range(8):
            if x_rights[x] + error <= chess_x_image[i] <= x_rights[x + 1] - error:
                x_fail = True
        for y in range(9):
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


def valid_move_rook(st, si, sj, di, dj):
    # Nếu không ở vị trí thẳng hàng theo bất kì trục nào thì False
    if si != di and sj != dj:
        return False
    # Nếu ở bên cạnh
    if (abs(si - di) == 1 and sj == dj) or (abs(sj - dj) == 1 and si == di):
        return True
    # Chạy dọc theo từng trục, nếu có quân cờ cản đường thì trả về False
    if si == di:  # di ngang
        for idj in range(sj + 1, dj):
            if st[si, idj] != '.':
                return False
    elif sj == dj:
        for idi in range(si + 1, di):
            if st[idi, sj] != '.':
                return False
    return True


def valid_move_horse(st, si, sj, di, dj):
    # Nếu không ở đúng vị trí so với nhau
    if (abs(si - di) == 2 and abs(sj - dj) != 1) or (abs(si - di) == 1 and abs(sj - dj) != 2):
        return False
    if (si - 2 == di and st[si - 1][sj] != '.') \
            or (si + 2 == di and st[si + 1][sj] != '.') \
            or (sj - 2 == dj and st[si][sj - 1] != '.') \
            or (sj + 2 == dj and st[si][sj + 1] != '.'):
        return False
    return True


def valid_move_elephant(st, si, sj, di, dj):
    if abs(si - di) != 2 or abs(sj - dj) != 2:
        return False
    if st[(si + di) / 2][(sj + dj) / 2] != '.':
        return False
    return True


def valid_move_advisor(st, si, sj, di, dj):
    if abs(si - di) != 1 or abs(sj - dj) != 1:
        return False
    return True


def valid_move_pawn(st, si, sj, di, dj):
    # chỉ xét quân đen (quân của người chơi)
    return (si + 1 == di and sj == dj) or ((si == di) and (si > 5) and abs(sj - dj) == 1)


def valid_move_cannon(st, si, sj, di, dj):
    # giống xe
    # Nếu không thẳng hàng thì sai
    if si != di and sj != dj:
        return False
    # Nếu cạnh nhau là sai
    if (abs(si - di) == 1 and sj == dj) or (abs(sj - dj) == 1 and si == di):
        return False
    # chạy dọc theo từng trục, nếu có != 1 quân cờ cản đường thì trả về False
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


def valid_move(previous_state, state):
    if not valid_position(state):
        print('Trạng thái bàn cờ không hợp lệ: Thiếu - thừa quân hoặc quân không đúng vị trí cho phép')
        return None

    champ_name = ''
    found_src, found_dst = 0, 0
    src_i, src_j, dst_i, dst_j = 0, 0, 0, 0
    for i in range(10):
        for j in range(9):
            if previous_state[i][j] != '.' and state[i][j] == '.':
                src_i, src_j = i, j
                champ_name = previous_state[i][j]  # tên quân cờ
                found_src += 1
                if found_src > 1:
                    return False
            elif (previous_state[i][j] != '.' and previous_state[i][j] != state[i][j]) or (
                    previous_state[i][j] == '.' and state[i][j] != '.'):
                dst_i, dst_j = i, j
                found_dst += 1
                if found_dst > 1:
                    return False
    if champ_name == '' or src_i == 0 or src_j == 0 or dst_i == 0 or dst_j == 0:
        return False
    return (champ_name.capitalize() == 'R' and valid_move_rook(previous_state, src_i, src_j, dst_i, dst_j)) \
        or (champ_name.capitalize() == 'H' and valid_move_horse(previous_state, src_i, src_j, dst_i, dst_j)) \
        or (champ_name.capitalize() == 'E' and valid_move_elephant(previous_state, src_i, src_j, dst_i, dst_j)) \
        or (champ_name.capitalize() == 'A' and valid_move_advisor(previous_state, src_i, src_j, dst_i, dst_j)) \
        or (champ_name.capitalize() == 'K' and valid_move_king(previous_state, src_i, src_j, dst_i, dst_j)) \
        or (champ_name.capitalize() == 'C' and valid_move_cannon(previous_state, src_i, src_j, dst_i, dst_j)) \
        or (champ_name.capitalize() == 'P' and valid_move_pawn(previous_state, src_i, src_j, dst_i, dst_j))
