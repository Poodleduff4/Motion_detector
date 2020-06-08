import time
import copy
import pynput.keyboard as keyboard
from pynput.keyboard import Key, Listener
import cv2
import numpy as np
delay_time = 0.1
printGay = False

cam = cv2.VideoCapture(0)
# cv2.namedWindow("test")
img_counter = 0
last_frame = np.zeros(shape=(480, 640, 3))


def on_press(key):
    global delay_time, printGay
    if key == Key.f1:
        delay_time = 0.1
    elif key == Key.f2:
        delay_time = 0.5
    if key == Key.f3:
        delay_time = 1

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    ret, frame = cam.read()

    cv2.imshow("test", frame)

    current_frame = frame

    # print(type(current_frame))

    cv2.imshow("test", current_frame)
    # print(np.array_equal(current_frame, last_frame))
    # print("Dimensions: ", end='')
    # print(current_frame.ndim)
    # print("Shape: ", end='')
    # print(current_frame.shape)
    # print("Size: ", end='')
    # print(current_frame.size)

    if np.allclose(current_frame, last_frame, 1, 50):
        print("Similar values, No motion")
    else:
        print("Motion")

    print("Delay time: " + str(delay_time))

    k = cv2.waitKey(1)

    if k == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    time.sleep(delay_time)
    last_frame = copy.deepcopy(current_frame)
cam.release()
cv2.destroyAllWindows()
