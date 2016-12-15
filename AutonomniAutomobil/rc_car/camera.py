# Author: Nina Marjanovic
# Description: Streams video using IP Webcam Android application

#Start app>Start server>Run script
#Press Esc to stop the script

import numpy as np
import cv2
import urllib2


class Camera(object):
    def __init__(self, host='192.168.0.103:8080'):
        self.host = host

    def stream(self):
        hoststr = 'http://{0}/video'.format(self.host)
        stream = urllib2.urlopen(hoststr)
        bytes = ''
        while True:
            bytes += stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                im_gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                cv2.imshow(hoststr, im_bw)
                if cv2.waitKey(1) == 27:
                    exit(0)

camera = Camera()
camera.stream()
