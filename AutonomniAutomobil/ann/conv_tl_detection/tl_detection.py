# Author: Nina Marjanovic

import numpy as np
import cv2
from PIL import Image

def detect(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 2)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if 6 >= len(approx) >= 3 and 6000 > area > 1000 and not cv2.isContourConvex(cnt):

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

            circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 20, param1=70, param2=30, minRadius=0,
                                       maxRadius=50)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (c_x, c_y, r) in circles:
                    if x <= c_x <= x+w and y <= c_y <= y+h:
                        cropped = img[c_y - 5:c_y + 5, c_x - 5:c_x + 5]
                        red = np.average(np.average(cropped, 0), 0)[2]
                        if red > 100:
                            #red light
                            cv2.circle(img, (c_x, c_y), r, (0, 0, 255), 4)
                            cv2.rectangle(img, (c_x - 5, c_y - 5), (c_x + 5, c_y + 5), (0, 0, 255), -1)
                            # print cropped
                        else:
                            #green light
                            cv2.circle(img, (c_x, c_y), r, (0, 255, 0), 4)
                            cv2.rectangle(img, (c_x - 5, c_y - 5), (c_x + 5, c_y + 5), (0, 255, 0), -1)




