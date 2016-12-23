# Author: Branislav Vezilic
# Description: Definicija opencv funkcija za obradu slika i detektovanje linija

import cv2
import numpy as np
from warnings import warn


def read_img(path):
    return cv2.imread(path, cv2.IMREAD_COLOR)


def show_img(img):
    cv2.imshow('put',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def img_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def edges(gray):
    return cv2.Canny(gray, 50, 150)


def lines(img_edges):
    return cv2.HoughLines(img_edges, 1, np.pi/180, 50)


def detect_lames(img):
    img = remove_upper(img, 50)
    lane = lines(edges(img_to_gray(img)))
    if lane is None:
        warn('Nema linija')
        return img
    for i in range(len(lane)):
        rho = lane[i][0][0]
        theta = lane[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img


def remove_upper(img, percent):
    print img.shape[0]*percent/100
    crop_img = img[img.shape[0]*percent/100:, 0:]
    return crop_img


def test():
    img = read_img('C:/Users/Bane Vezilic/Desktop/road.jpg')
    remove_upper(img, 50)

#test()




