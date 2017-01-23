#autor: Branislav Vezilic

import numpy as np
import cv2


def detect(img):
    '''
    :param img: image in BGR color space
    :return:
        dist - distance to 'STOP' sign
        img - image with detected 'STOP' sign
    '''
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of red color in HSV
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Bitwise-OR of the masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Initialize distance
    dist = -1

    # Finding contours in mask image
    img2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        # Conditions that have to be satisfied for valid 'STOP' sign
        if area > 200 and x > mask.shape[1]/2:
            # Draw rectangle over 'STOP' sign
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Calculate distance to 'STOP' sign
            dist = distance(w)

    return dist, img


def distance(width_in_pix):
    '''
    :param width_in_pix: width of object in image
    :return: distance to 'STOP' sign
    '''
    known_distance = 8.0
    known_width = 4.0
    focal_length = get_focal_length(known_distance, known_width)
    return (known_width * focal_length) / width_in_pix


def get_focal_length(known_distance, known_width, width_in_pixels=80):
    return (width_in_pixels * known_distance) / known_width


def test():
    path = "C:\Users\Bane Vezilic\Desktop\sign.jpg"
    dist, img = detect(cv2.imread(path))
    print dist
    cv2.imshow('STOP', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#test()
