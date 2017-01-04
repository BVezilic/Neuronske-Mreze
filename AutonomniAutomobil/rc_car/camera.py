# Author: Nina Marjanovic
# Description: Streams video using IP Webcam Android application

#Start app>Start server>Run script
#Press Esc to stop the script

from __future__ import print_function
import numpy as np
import cv2
import urllib2
import lane_detector as fl
from simulator.simulator import Simulator
from multiprocessing import Pool



class Camera(object):
    def __init__(self, host='192.168.1.8:8080'):
        self.host = host
        self.simulator = Simulator()

    def stream(self):
        hoststr = 'http://{0}/video'.format(self.host)
        stream = urllib2.urlopen(hoststr)
        f = open('training_data', 'a')
        bytes = ''
        while True:
            bytes += stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                img, left_distance, right_distance,  left_line, right_line = fl.detect_lanes(img)
                cv2.imshow(hoststr, img)
                if left_distance is False:
                    left_distance = -1
                if right_distance is False:
                    right_distance = -1
                f.write(str(left_distance) + ',' + str(right_distance) + ',1,0,0\n')
                #1(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                if cv2.waitKey(1) == 27:
                    f.close()
                    exit(0)


camera = Camera()


def run_camera():
    camera.stream()


def simulation():
    camera.simulator.simulate()


def main():
    run_camera()
    """
    pool = Pool(processes=2)
    pool.apply_async(run_camera)
    pool.apply_async(simulation)
    pool.close()
    pool.join()
    """

if __name__ == '__main__':
    main()
