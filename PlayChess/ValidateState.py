def wrong_position(chess_x_image, chess_y_image):  # error 1
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


def valid_state(state):
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


def define_move(previous_state, state):
    found_src, found_dst = 0, 0
    src_x, src_y, dst_x, dst_y = '', 0, '', 0
    for i in range(10):
        for j in range(9):
            if previous_state[i, j] != '.' and state[i][j] != '.':
                src_x = chr(ord('a') + j - 1)
                src_y = i
                found_src += 1
                if found_src > 1:
                    return '', 0, '', 0
            elif (previous_state[i, j] != '.' and previous_state[i][j] != state[i][j]) or (previous_state[i, j] == '.' and state[i][j] != '.'):
                dst_x = chr(ord('a') + j - 1)
                dst_y = i
                found_dst += 1
                if found_dst > 1:
                    return '', 0, '', 0
    return src_x, src_y, dst_x, dst_y
