import numpy as np
import cv2
import glob

from Const.VisionConst import *

chessboardSize = (7, 7)
frame_size = resolution


def save_calibration_result():
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

    size_of_chessboard_squares_mm = 25
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('.\\CalibrateCamera\\*.jpg')

    for image in images:
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(400)

    cv2.destroyAllWindows()
    ret, camera_matrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame_size, None, None)

    np.savetxt('.\\calib_camera\\camera_matrix.txt', camera_matrix)
    np.savetxt('.\\calib_camera\\dist.txt', dist)


# pickle.dump((cameraMatrix, dist), open("calibration.pkl", "wb"))
# pickle.dump(cameraMatrix, open("cameraMatrix.pkl", "wb"))
# pickle.dump(dist, open("dist.pkl", "wb"))


def calibrate_image(image):
    # load calibration matrix, vector
    camera_matrix = np.loadtxt('.\\CalibrateCamera\\camera_matrix.txt')
    dist = np.loadtxt('.\\CalibrateCamera\\dist.txt')

    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist, (w, h), 1, (w, h))

    # undistort
    dst = cv2.undistort(image, camera_matrix, dist, None, new_camera_matrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    return dst


def calibrate_remap_image(image):
    # load calibration matrix, vector
    camera_matrix = np.loadtxt('.\\CalibrateCamera\\camera_matrix.txt')
    dist = np.loadtxt('.\\CalibrateCamera\\dist.txt')

    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist, (w, h), 1, (w, h))

    # Undistort with Remapping
    mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, dist, None, new_camera_matrix, (w, h), 5)
    dst = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    # x, y, w, h = roi
    # dst = dst[y:y + h, x:x + w]
    return dst


def capture_image(save_path, prefix):
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    num = 0
    while True:
        _, image = capture.read()
        k = cv2.waitKey(5)
        if k == 27:
            break
        elif k == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite(save_path + prefix + str(num) + '.jpg', image)
            print("image saved!" + str(num))
            num += 1
        show_image = cv2.resize(image, (960, 540))
        cv2.imshow('Img', show_image)
    # Release and destroy all windows before termination
    capture.release()
    cv2.destroyAllWindows()


def fix_real(x, y):
    size = len(x)
    x0, y0 = 184, 284
    xs, ys = x - 184, y - 204
    r = np.sqrt(xs * xs + ys * ys)
    # print(r)
    dx = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0])
    dy = np.array([0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0])
    m = np.array([60, 80, 110, 130, 140, 150, 160, 170, 180, 200, 230, 260])
    for i in range(size):
        # inc x, inc y
        if (m[0] < r[i] <= m[1]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[0]
            y[i] += dy[0]
        elif (m[1] < r[i] <= m[2]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[1]
            y[i] += dy[1]
        elif (m[2] < r[i] <= m[3]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[2]
            y[i] += dy[2]
        elif (m[3] < r[i] <= m[4]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[3]
            y[i] += dy[3]
        elif (m[4] < r[i] <= m[5]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[4]
            y[i] += dy[4]
        elif (m[5] < r[i] <= m[6]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[5]
            y[i] += dy[5]
        elif (m[6] < r[i] <= m[7]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[6]
            y[i] += dy[6]
        elif (m[7] < r[i] <= m[8]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[7]
            y[i] += dy[7]
        elif (m[8] < r[i] <= m[9]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[8]
            y[i] += dy[8]
        elif (m[9] < r[i] <= m[10]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[9]
            y[i] += dy[9]
        elif (m[10] < r[i] <= m[11]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[10]
            y[i] += dy[10]
        elif (m[11] < r[i]) and (x[i] < x0) and (y[i] < y0):
            x[i] += dx[11]
            y[i] += dy[11]
        # inc x, dec y
        elif (m[0] < r[i] <= m[1]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[0]
            y[i] -= dy[0]
        elif (m[1] < r[i] <= m[2]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[1]
            y[i] -= dy[1]
        elif (m[2] < r[i] <= m[3]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[2]
            y[i] -= dy[2]
        elif (m[3] < r[i] <= m[4]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[3]
            y[i] -= dy[3]
        elif (m[4] < r[i] <= m[5]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[4]
            y[i] -= dy[4]
        elif (m[5] < r[i] <= m[6]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[5]
            y[i] -= dy[5]
        elif (m[6] < r[i] <= m[7]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[6]
            y[i] -= dy[6]
        elif (m[7] < r[i] <= m[8]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[7]
            y[i] -= dy[7]
        elif (m[8] < r[i] <= m[9]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[8]
            y[i] -= dy[8]
        elif (m[9] < r[i] <= m[10]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[9]
            y[i] -= dy[9]
        elif (m[10] < r[i] <= m[11]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[10]
            y[i] -= dy[10]
        elif (m[11] < r[i]) and (x[i] < x0) and (y[i] > y0):
            x[i] += dx[11]
            y[i] -= dy[11]
        # dec x, dec y
        elif (m[0] < r[i] <= m[1]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[0]
            y[i] -= dy[0]
        elif (m[1] < r[i] <= m[2]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[1]
            y[i] -= dy[1]
        elif (m[2] < r[i] <= m[3]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[2]
            y[i] -= dy[2]
        elif (m[3] < r[i] <= m[4]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[3]
            y[i] -= dy[3]
        elif (m[4] < r[i] <= m[5]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[4]
            y[i] -= dy[4]
        elif (m[5] < r[i] <= m[6]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[5]
            y[i] -= dy[5]
        elif (m[6] < r[i] <= m[7]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[6]
            y[i] -= dy[6]
        elif (m[7] < r[i] <= m[8]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[7]
            y[i] -= dy[7]
        elif (m[8] < r[i] <= m[9]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[8]
            y[i] -= dy[8]
        elif (m[9] < r[i] <= m[10]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[9]
            y[i] -= dy[9]
        elif (m[10] < r[i] <= m[11]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[10]
            y[i] -= dy[10]
        elif (m[11] < r[i]) and (x[i] > x0) and (y[i] > y0):
            x[i] -= dx[11]
            y[i] -= dy[11]
        # dec x, inc y
        elif (m[0] < r[i] <= m[1]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[0]
            y[i] += dy[0]
        elif (m[1] < r[i] <= m[2]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[1]
            y[i] += dy[1]
        elif (m[2] < r[i] <= m[3]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[2]
            y[i] += dy[2]
        elif (m[3] < r[i] <= m[4]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[3]
            y[i] += dy[3]
        elif (m[4] < r[i] <= m[5]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[4]
            y[i] += dy[4]
        elif (m[5] < r[i] <= m[6]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[5]
            y[i] += dy[5]
        elif (m[6] < r[i] <= m[7]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[6]
            y[i] += dy[6]
        elif (m[7] < r[i] <= m[8]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[7]
            y[i] += dy[7]
        elif (m[8] < r[i] <= m[9]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[8]
            y[i] += dy[8]
        elif (m[9] < r[i] <= m[10]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[9]
            y[i] += dy[9]
        elif (m[10] < r[i] <= m[11]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[10]
            y[i] += dy[10]
        elif (m[11] < r[i]) and (x[i] > x0) and (y[i] < y0):
            x[i] -= dx[11]
            y[i] += dy[11]

    x = (np.rint(x)).astype(int)
    y = (np.rint(y)).astype(int)
    return x, y
