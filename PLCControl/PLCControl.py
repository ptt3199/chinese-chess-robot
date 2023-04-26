import OpenOPC
import pywintypes
import time
from math import *

pywintypes.datetime = pywintypes.TimeType
opc = OpenOPC.client()
opc.connect('Kepware.KEPServerEX.V6')

""" Play chess """


def move(x1, y1, x2, y2):
    opc.write(('Channel2.Device1.D13', x1))
    opc.write(('Channel2.Device1.D14', y1))
    opc.write(('Channel2.Device1.D15', x2))
    opc.write(('Channel2.Device1.D16', y2))
    d2 = 0.2 + 0.0043 * sqrt(2) * min(abs(x1 + 10), abs(y1 - 15)) + 0.0025 * (
            max(abs(x1 + 10), abs(y1 - 15)) - min(abs(x1 + 10), abs(y1 - 15)))
    d3 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 - x1), abs(y2 - y1)) + 0.0025 * (
            max(abs(x2 - x1), abs(y2 - y1)) - min(abs(x2 - x1), abs(y2 - y1)))
    d4 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 + 10), abs(y2 - 15)) + 0.0025 * (
            max(abs(x2 + 10), abs(y2 - 15)) - min(abs(x2 + 10), abs(y2 - 15)))
    opc.write(('Channel2.Device1.Y10', 0))
    opc.write(('Channel2.Device1.Y7', 0))

    # HOME to (1)
    opc.write(('Channel2.Device1.M2', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d2)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)

    # (1) to (2)
    opc.write(('Channel2.Device1.M3', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d3)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)

    # (2) to HOME
    opc.write(('Channel2.Device1.M8', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d4)
    opc.write(('Channel2.Device1.Y10', 1))
    opc.write(('Channel2.Device1.Y7', 1))


def capture(x1, y1, x2, y2):
    opc.write(('Channel2.Device1.D13', x1))
    opc.write(('Channel2.Device1.D14', y1))
    opc.write(('Channel2.Device1.D15', x2))
    opc.write(('Channel2.Device1.D16', y2))
    d3 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 - x1), abs(y2 - y1)) + 0.0025 * (
            max(abs(x2 - x1), abs(y2 - y1)) - min(abs(x2 - x1), abs(y2 - y1)))
    d4 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 + 10), abs(y2 - 15)) + 0.0025 * (
            max(abs(x2 + 10), abs(y2 - 15)) - min(abs(x2 + 10), abs(y2 - 15)))
    opc.write(('Channel2.Device1.Y10', 0))
    opc.write(('Channel2.Device1.Y7', 0))

    # HOME to (2)
    opc.write(('Channel2.Device1.M4', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d4)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)

    # (2) to DROP
    opc.write(('Channel2.Device1.M5', True))
    D17 = opc.read('Channel2.Device1.D17')
    D18 = opc.read('Channel2.Device1.D18')
    d5 = 0.2 + 0.0043 * sqrt(2) * min(abs(D17[0] - x2), abs(D18[0] - y2)) + 0.0025 * (
            max(abs(D17[0] - x2), abs(D18[0] - y2)) - min(abs(D17[0] - x2), abs(D18[0] - y2)))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d5)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)

    # DROP to (1)
    opc.write(('Channel2.Device1.M6', True))
    d6 = 0.2 + 0.0043 * sqrt(2) * min(abs(D17[0] - x1), abs(D18[0] - y1)) + 0.0025 * (
            max(abs(D17[0] - x1), abs(D18[0] - y1)) - min(abs(D17[0] - x1), abs(D18[0] - y1)))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d6)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)

    # (1) to (2)
    opc.write(('Channel2.Device1.M3', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d3)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)

    # (2) to HOME
    opc.write(('Channel2.Device1.M8', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d4)
    opc.write(('Channel2.Device1.Y10', 1))
    opc.write(('Channel2.Device1.Y7', 1))


""" Set up chess board """


def home2start(x1, y1):
    opc.write(('Channel2.Device1.D13', x1))
    opc.write(('Channel2.Device1.D14', y1))
    d2 = 0.2 + 0.0043 * sqrt(2) * min(abs(x1 + 10), abs(y1 - 15)) + 0.0025 * (
            max(abs(x1 + 10), abs(y1 - 15)) - min(abs(x1 + 10), abs(y1 - 15)))
    opc.write(('Channel2.Device1.Y10', 0))
    opc.write(('Channel2.Device1.M2', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d2)


def end2home(x2, y2):
    opc.write(('Channel2.Device1.D15', x2))
    opc.write(('Channel2.Device1.D16', y2))
    d4 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 + 10), abs(y2 - 15)) + 0.0025 * (
            max(abs(x2 + 10), abs(y2 - 15)) - min(abs(x2 + 10), abs(y2 - 15)))
    opc.write(('Channel2.Device1.M8', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d4)
    opc.write(('Channel2.Device1.Y10', 1))
    opc.write(('Channel2.Device1.Y7', 1))


def point2point(x1, y1, x2, y2):
    opc.write(('Channel2.Device1.D13', x1))
    opc.write(('Channel2.Device1.D14', y1))
    opc.write(('Channel2.Device1.D15', x2))
    opc.write(('Channel2.Device1.D16', y2))
    d3 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 - x1), abs(y2 - y1)) + 0.0025 * (
            max(abs(x2 - x1), abs(y2 - y1)) - min(abs(x2 - x1), abs(y2 - y1)))
    opc.write(('Channel2.Device1.M3', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d3)


def pick_drop(x1, y1, x2, y2):
    opc.write(('Channel2.Device1.D13', x1))
    opc.write(('Channel2.Device1.D14', y1))
    opc.write(('Channel2.Device1.D15', x2))
    opc.write(('Channel2.Device1.D16', y2))
    d3 = 0.2 + 0.0043 * sqrt(2) * min(abs(x2 - x1), abs(y2 - y1)) + 0.0025 * (
            max(abs(x2 - x1), abs(y2 - y1)) - min(abs(x2 - x1), abs(y2 - y1)))
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)
    opc.write(('Channel2.Device1.M3', True))
    opc.write(('Channel2.Device1.M1', True))
    time.sleep(d3)
    opc.write(('Channel2.Device1.M7', True))
    time.sleep(0.8)


def red_lamp(a):
    opc.write(('Channel2.Device1.Y11', a))


def yellow_lamp(a):
    opc.write(('Channel2.Device1.Y7', a))


def push_green_button():
    d25_init = opc.read('Channel2.Device1.D25')
    check = d25_init[0]
    while True:
        d25 = opc.read('Channel2.Device1.D25')
        if d25[0] != check:
            return True


def push_yellow_button():
    d26_init = opc.read('Channel2.Device1.D26')
    check = d26_init[0]
    while True:
        d26 = opc.read('Channel2.Device1.D26')
        if d26[0] != check:
            return True


def check_green_button():
    d25 = opc.read('Channel2.Device1.D25')
    return d25[0]


def check_yellow_button():
    d26 = opc.read('Channel2.Device1.D26')
    return d26[0]
