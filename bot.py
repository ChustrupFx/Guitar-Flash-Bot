import time
import cv2
import numpy as np
from PIL import ImageGrab, ImageEnhance
from pynput.keyboard import Controller
from time import sleep


def getSensorPositions():
    firstSensorPosition = [268, 425]
    sensorsSpacement = 70

    sensorPositions = []

    for index in range(0, 5):
        xPos = firstSensorPosition[0] + (index * sensorsSpacement)
        yPos = firstSensorPosition[1]

        sensorPositions.append([xPos, yPos])

    return sensorPositions


def createMask(originalImage):
    colorsRanges = [
        [(0, 120, 0), (71, 255, 71)],  # Green
        [np.array([0, 169, 169]), np.array([40, 255, 255])],  # Yellow
        [(162, 65, 0), (255, 97, 0)],  # Blue
        [(0, 100, 167), (81, 186, 255)],  # Orange
        [np.array([0, 0, 105]), np.array([81, 81, 255])],  # Red
    ]

    mask = None
    for darker, lighter in colorsRanges:
        newMask = cv2.inRange(originalImage, darker, lighter)
        if mask is not None:
            mask = cv2.bitwise_or(mask, newMask)
        else:
            mask = newMask

    return mask


startTime = time.time()
keyboardController = Controller()


while True:

    guitarFlashBounds = ((380, 251), (1197, 827))

    kernel = np.ones((5, 5), np.uint8)

    image = ImageGrab.grab(bbox=(
        guitarFlashBounds[0][0], guitarFlashBounds[0][1], guitarFlashBounds[1][0], guitarFlashBounds[1][1]))

    brightnessPILEnhancer = ImageEnhance.Brightness(image)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mask = createMask(image)

    # canny = cv2.Canny(mask, 100, 200)

    image_dilation = cv2.dilate(mask, kernel, iterations=3)
    # blur = cv2.medianBlur(image_dilation, 1)

    sensorPositions = getSensorPositions()

    # for posIndex in range(len(sensorPositions)):
    #     y, x = [sensorPositions[posIndex][1], sensorPositions[posIndex][0]]
    #     guitarFlashPossibleKeyboardInputs = ['a', 's', 'j', 'k', 'l']

    #     posColor = image_dilation[y, x]

    #     keyToPress = guitarFlashPossibleKeyboardInputs[posIndex]

    #     if posColor == 255:
    #         keyboardController.press(keyToPress)
    #     else:
    #         keyboardController.release(keyToPress)

    # # cv2.circle(
    #     image_dilation, (x, y), 1, (255, 0, 0), -1)

    cv2.imshow('Imagem sem filtro', image)
    cv2.imshow('mask', mask)
    cv2.imshow('Branco estourado', image_dilation)
    # print('FPS:', 1 / (time.time() - startTime))
    startTime = time.time()

    if cv2.waitKey(1) == ord('q'):
        break
