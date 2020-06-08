import time
import cv2
import numpy as np
import copy
import threading
import sys
import msvcrt
import pynput.keyboard as keyboard
from pynput.keyboard import Key, Listener



cam = cv2.VideoCapture(0)
ret, frame = cam.read()
delay_time = 0.1

run = True

print()

shape = frame.shape
size = str(frame.size)
rows = str(shape[0])
columns = str(shape[1])
dims = str(shape[2])

print("Size: " + size)
print("Rows: " + rows)
print("Cols: " + columns)
print("Dims: " + dims)
print()

last_frame = np.zeros(shape=(480, 640, 3))

def on_press(key):
    global delay_time, printGay
    if key == Key.f1:
        delay_time = 0.5
    elif key == Key.f2:
        delay_time = 0.1
    if key == Key.f3:
        delay_time = 2

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

def readcam():
    global ret, frame
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k == 27:
            # ESC pressed
            print("Escape hit, closing...")
            cam.release()
            cv2.destroyAllWindows()
            sys.exit(0)
        time.sleep(delay_time)


camObj = threading.Thread(target=readcam)
camObj.start()
avgDifPrev = 0
avgDif = 0
while True:

    current_frame = frame
    # current_frame = np.empty([480, 640, 3])
    # current_frame.fill(255)
    start_time = time.time()
    for a in range(0, shape[0], 4):
        for b in range(0, shape[1], 4):
            # print("Current " + str(current_frame[a][b][0]) + ", " + str(current_frame[a][b][1]) + ", " + str(current_frame[a][b][2]), end=' / ')
            # print("Last " + str(last_frame[a][b][0]) + ", " + str(last_frame[a][b][1]) + ", " + str(last_frame[a][b][2]))

            rDif = current_frame[a][b][0] - last_frame[a][b][0]
            gDif = current_frame[a][b][1] - last_frame[a][b][1]
            bDif = current_frame[a][b][2] - last_frame[a][b][2]
            # print("Diff " + str(rDif) + ", " + str(gDif) + ", " + str(bDif))
            avgDif += (rDif + gDif + bDif) / 3
            # msvcrt.getch()
    end_time = time.time()
    # 0.14s without any printing

    avgDif /= shape[0] * shape[1]
    print("Prev: " + str(avgDifPrev))
    print("Curr: " + str(avgDif))
    print("Average Difference " + str(abs(avgDif - avgDifPrev)))
    # print("Time: " + str(end_time-start_time))
    last_frame = copy.deepcopy(current_frame)
    avgDifPrev = copy.deepcopy(avgDif)
    time.sleep(delay_time)

# """
# Times:
# printing out each pixel and it's RGB components : 57s
# just calculating the pixel averages : 0.7s
# reading an image from the camera : 0.45s
# reading and calculating one image : 1.1s - 1.2s
# """
