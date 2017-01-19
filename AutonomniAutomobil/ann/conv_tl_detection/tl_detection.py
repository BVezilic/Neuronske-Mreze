# Author: Nina Marjanovic

import numpy as np
import cv2


def detect(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if len(approx) == 4 and area > 10 and not cv2.isContourConvex(cnt):
            rect = cv2.minAreaRect(cnt)
            print rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            #print box
            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

            circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 20, param1=70, param2=30, minRadius=0,
                                       maxRadius=50)
            # ensure at least some circles were found
            if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    if True:
                        # draw the circle in the output image, then draw a rectangle
                        # corresponding to the center of the circle
                        cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            #cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)




