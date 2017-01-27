# Author: Nina Marjanovic
# Description: Detecting traffic lights using cascade classifier

import numpy as np
import cv2



def detect(img):
    tl_cascade = cv2.CascadeClassifier('../object_detection/tl_detection_cascade.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    traffic_lights = tl_cascade.detectMultiScale(gray, 1.3, 5)
    print len(traffic_lights)
    for (x,y,w,h) in traffic_lights:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    #cv2.imshow('img',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()