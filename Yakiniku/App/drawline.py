import cv2
import numpy as np
import matplotlib.pyplot as plt

global img


def drawline(fro, dst, col):
    global img
    cv2.line(img, fro, dst, col, 1)


def openpic(file_name):
    global img
    img = cv2.imread(file_name)


def writepic(file_name):
    global img
    cv2.imwrite(file_name, img)


if __name__ == '__main__':
    file_name = "C:/Coding/SOA/pic/t3.jpg"
    openpic(file_name)
    drawline((20, 20), (50, 50), (0, 255, 0))
    writepic("ans1.jpg")
    # cv2.line(img, (20, 20), (100, 100), (0, 255, 0), 3)
