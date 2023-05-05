import cv2
import csv
import numpy as np
from keras.utils.image_utils import img_to_array
from keras.models import load_model

from CalibrateCamera.Calibrate import *
from Network.Network import *
from Const.VisionConst import *
from Utils.VisionUtils import *

""" Load model """
model = load_model('RecognizeModel\\model.h5')
print("RecognizeModel loaded!------------------------------------------")


""" Load server """
server_recognize = Server(8082)
print('Chess Recognize Server: ON')
print('Listening...')
server_recognize.accept()
print('Connected!')

""" Recognize chess champ """
train_size = image_train_size
# edges
left, right, top, bottom = raw_left, raw_right, raw_top, raw_bottom


def define_chess_champ():
    """preprocessing image"""
    image = cv2.imread('.\\Camera\\temp.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to gray
    image = calibrate_remap_image(image)  # Calibrate image

    image = image[top:bottom, left:right]  # Remove leftovers
    # cv2.imwrite('.\\Camera\\blah.jpg', image)
    image = cv2.resize(image, (image_width, image_height))  # Need to rescale to 905:1010 = 368:411
    width, height = image.shape

    """hough circle"""
    radius = round(0.288 * chess_piece_size_image)
    circle_min_distance = round(2 * radius)
    circles = cv2.HoughCircles(
        image,  # input image, greyscale
        cv2.HOUGH_GRADIENT,
        1.0,  # dp, the inverse ratio of resolution
        circle_min_distance,  # Minimum distance between detected centers
        param1=300,
        param2=15,
        minRadius=round(radius * .98),
        maxRadius=round(radius * 1.01)
    )
    circles = np.uint16(np.around(circles))

    """prepare data for recognizing"""
    count_circle = 0
    data, chess_int, chess_x, chess_y = [], [], [], []
    for circle in circles[0, :]:
        (x, y, _) = circle
        center = (x, y)
        chess_x.append(x)
        chess_y.append(y)
        cv2.circle(image, center, radius, (0, 0, 0), 2)
        count_circle = count_circle + 1
        # Crop circles
        mask = np.zeros((width, height), np.uint8)
        cv2.circle(mask, center, radius, (255, 255, 255), thickness=-1)
        masked_im = cv2.bitwise_and(image, image, mask=mask)
        cropped_im = masked_im[y - radius:y + radius, x - radius:x + radius]
        binary_chess_champ = convert_binary(cv2.resize(cropped_im, (train_size, train_size)))
        data.append(img_to_array(binary_chess_champ))
    data = np.array(data)
    data = data / 255.0
    for i in range(len(data)):
        img = data[i]
        img = np.expand_dims(img, 0)
        output = model.predict(img)
        chess_int.append(output.argmax())

    chess_x, chess_y = np.array(chess_x), np.array(chess_y)
    chess_x_board = np.round(width_real / image_width * chess_x, 1)
    chess_y_board = np.round(409 - height_real / image_height * chess_y, 1)
    chess_x_board, chess_y_board = fix_real(chess_x_board, chess_y_board)

    size = len(chess_int)
    with open('.\\Camera\\data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(size):
            writer.writerow([str(chess_x_board[i]), str(chess_y_board[i]), str(chess_int[i])])
    print('Done Recognizing', len(chess_int), 'found')


while True:
    data_receive = server_recognize.receive()
    if data_receive[0] == 'Go':
        define_chess_champ()
    """answer client"""
    data_send = ['Done']
    server_recognize.send(data_send)
