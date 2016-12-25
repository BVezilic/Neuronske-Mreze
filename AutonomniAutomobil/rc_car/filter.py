# Author: Branislav Vezilic
# Description: Definicija opencv funkcija za obradu slika i detektovanje linija

import cv2
import numpy as np
import random
from warnings import warn


def read_img(path):
    """Calls opencv function for reading image"""
    return cv2.imread(path, cv2.IMREAD_COLOR)


def show_img(img):
    """Shows image in new window. Press ESC to close it."""
    cv2.imshow('put',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def img_to_gray(img):
    """Calls opencv function for transforming image to gray-scale image"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def edges(gray):
    """Calls opencv function for transforming gray-scale image into binary image with detected edges"""
    return cv2.Canny(gray, 50, 150)


def lines(img_edges):
    """Calls opencv function for transforming binary image in to list of lines found in image"""
    return cv2.HoughLines(img_edges, 1, np.pi/180, 50)


def line(p1, p2):
    """Creates three coefficient from two points (line)"""
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C


def intersection(L1, L2):
    """Checks if two lines have intersection. Returns x,y coordinates if true, otherwise returns false."""
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


def remove_upper(img, percent):
    """Crops image horizontally with given percentage"""
    crop_img = img[img.shape[0]*percent/100:, 0:]
    return crop_img


def is_valid_degree(theta, i1=(-80, -45), i2=(45, 80)):
    """Check if theta is in one of two intervals"""
    degree = theta * 180 / np.pi - 90
    if i1[0] < degree < i1[1] or i2[0] < degree < i2[1]:
        return True
    else:
        return False


def degree_interval(lanes):
    """Returns a new list with lines that have valid degree"""
    new_lanes = []
    for rho, theta in lanes:
        if is_valid_degree(theta):
            new_lanes.append([rho, theta])
    return new_lanes


def is_valid_position(point, border):
    """Check if X is in valid intervals"""
    if border[0][0] < point[0] < border[1][0]:
        return True
    else:
        return False


def difference_on_border(point, border):
    """Calculates how far is point from center of the border"""
    center_x = np.abs(border[0][0] - border[1][0])
    return point[0] - center_x


def detect_lanes(img):
    """Detectes lanes in image, finds those lines and returns one left and one right line"""
    #list that will contain valid right and left lines
    valid_left_lines = []
    valid_right_lines = []

    #crop image to show bottom half of image
    img = remove_upper(img, 50)

    #find lines in image
    lane = lines(edges(img_to_gray(img)))

    #border lines for validation
    left_border = [(30, 35), (60, 35)]
    right_border = [(120, 35), (150, 35)]

    #draw border lines on image
    cv2.line(img, left_border[0], left_border[1], (255, 0, 255), 1)
    cv2.line(img, right_border[0], right_border[1], (255, 0, 255), 1)

    #check if there are lines on image
    if lane is None:
        warn('Nema linija')
        return img

    #iterate through every line in image to find which one are valid
    for i in range(len(lane)):
        rho = lane[i][0][0]
        theta = lane[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)

        #check with left border
        left_intersection = intersection(line([x1, y1], [x2, y2]), line(left_border[0], left_border[1]))
        if left_intersection:
            if is_valid_position(left_intersection, left_border):
                valid_left_lines.append([tuple(lane[i][0]), left_intersection])
                #draw line
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            print 'WARRNING: No intersection on left border.'

        #check with right border
        right_intersection = intersection(line([x1, y1], [x2, y2]), line(right_border[0], right_border[1]))
        if right_intersection:
            if is_valid_position(right_intersection, right_border):
                valid_right_lines.append([tuple(lane[i][0]), right_intersection])
                #draw line
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            print 'WARRNING: No intersection on right border.'
        #print 'Linija:{0}, x1:{1}, y1:{2}, x2:{3}, y2:{4}'.format(i, x1, y1, x2, y2)

    #Choose one from valid left and right lines
    left_line = random.choice(valid_left_lines) if len(valid_left_lines) > 0 else False
    right_line = random.choice(valid_right_lines) if len(valid_right_lines) > 0 else False

    #Get distance from middle of the screen
    left_distance = (np.abs(left_line[1][0] - img.shape[1]/2)) if left_line else False
    right_distance = (np.abs(right_line[1][0] - img.shape[1]/2)) if right_line else False

    return img, left_distance, right_distance, left_line, right_line


def test():
    img = read_img('C:/Users/Bane Vezilic/Desktop/Untitled.jpg')
    img_lane, left_distance, right_distance, left_line, right_line = detect_lanes(img)
    show_img(img_lane)

#test()




