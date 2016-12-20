# Author: Branislav Vezilic
# Description: Definicija opencv funkcija za obradu slika i detektovanje linija

import cv2
import numpy as np


def read_img(path):
    return cv2.imread(path)


def img_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def edges(gray):
    return cv2.Canny(gray, 50, 150)


def lines(img_edges):
    return cv2.HoughLines(img_edges, 1, np.pi/180, 200)


def detect_lines(img):
    return lines(edges(img_to_gray(img)))


def test():
    read_img("")

