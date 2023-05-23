NUMSTRING = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
CHESSMAN = {'k', 'a', 'e', 'r', 'c', 'h', 'p', 'K', 'A', 'E', 'R', 'C', 'H', 'P'}
#
# raw_top = 45
# raw_bottom = 1037
# raw_left = 540
# raw_right = 1453
raw_top = 61
raw_bottom = 1061
raw_left = 543
raw_right = 1461
resolution = (1920, 1080)

# save model
model_path = ".\\RecognizeModel"

# recognize chess champ
image_width = 895
image_height = 1000
image_train_size = 120

# utils
chess_piece_size_image = 102
margin_image = 49

# chess_cn = [
#     # "一",
#     "将", "士", "象", "馬", "車", "包", "兵",
#     "帅", "仕", "相", "傌", "俥", "砲", "卒"
# ]
# chess_eng = [
#     'k', 'a', 'e', 'h', 'r', 'c', 'p',
#     'K', 'A', 'E', 'H', 'R', 'C', 'P'
# ]

chess_eng = [
    # 0   1    2    3    4    5    6
    'a', 'c', 'r', 'e', 'k', 'h', 'p',
    # 7   8    9    10   11   12   13
    'A', 'C', 'R', 'E', 'K', 'H', 'P'
]

# recognize
margin_real = 20
chess_piece_size_real = 41
height_real = 410
width_real = 368
