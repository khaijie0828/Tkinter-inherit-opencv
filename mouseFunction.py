import cv2
import numpy as np
import handTrackingModule as htm
import time
import autopy
from PyQt5.QtGui import QImage, QPixmap

wCam, hCam = 640, 480
frameR = 180
smooth = 5

preLocX, preLocY = 0, 0
curLocX, curLocY = 0, 0

capture = cv2.VideoCapture(0)
capture.set(3, wCam)
capture.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

clicked = False
rightClicked = False


def handTrackingFunction(frame):
    global preLocX, preLocY, curLocX, curLocY, clicked, rightClicked

    img = frame.copy()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Detect second and third fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        cv2.rectangle(img, (frameR, frameR - 50), (wCam - frameR, hCam - frameR), (255, 0, 0), 2)

        # Only second and third fingers = Move mode
        if all(fingers[i] == (1 if i in (1, 2) else 0) for i in range(5)):
            # Calculate the midpoint between index and middle fingers
            coorX = np.interp((x1 + x2) / 2, (frameR, wCam - frameR), (wScr, 0))
            coorY = np.interp((y1 + y2) / 2, (frameR - 50, hCam - frameR), (0, hScr))

            # Smoothen value
            curLocX = preLocX + (coorX - preLocX) / smooth
            curLocY = preLocY + (coorY - preLocY) / smooth

            # Move mouse
            if autopy.screen.is_point_visible(wScr - curLocX, curLocY):
                autopy.mouse.move(wScr - curLocX, curLocY)
            cv2.circle(img, (x1, y1), 10, (50, 183, 255), cv2.FILLED)
            preLocX, preLocY = curLocX, curLocY

            # Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Click if distance short and the click has not been executed
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
                if not clicked:
                    autopy.mouse.toggle(down=True)
                    time.sleep(0.1)
                clicked = True
            elif clicked:
                autopy.mouse.toggle(down=False)
                clicked = False

        # Right-click = third and fourth fingers
        if all(fingers[i] == (1 if i in (1, 2, 3) else 0) for i in range(5)):
            length, img, lineInfo = detector.findDistance(8, 16, img)
            if length < 50:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
                if not rightClicked:
                    autopy.mouse.toggle(button=autopy.mouse.Button.RIGHT, down=True)
                    time.sleep(0.2)
                rightClicked = True
            elif rightClicked:
                autopy.mouse.toggle(button=autopy.mouse.Button.RIGHT, down=False)
                rightClicked = False

    q_image = convert_frame_to_QImage(img)
    pixmap = QPixmap.fromImage(q_image)

    return pixmap


def convert_frame_to_QImage(frame):
    if frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, channel = frame.shape
    bytes_per_line = 3 * width
    q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return q_image
