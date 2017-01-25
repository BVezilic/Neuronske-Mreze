# Author: Nina Marjanovic
# Description: Generating training data

#TODO output


from __future__ import print_function

import urllib2
from multiprocessing import Pool

import cv2
import numpy as np

from object_detection import lane_detector as fl
from rc_car import controller


class Camera(object):
    def __init__(self, host='192.168.1.3:8080'):
        self.host = host

    def stream(self):
        f = open('training_data', 'a')
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
                img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                img, left_distance, right_distance,  left_line, right_line = fl.detect_lanes(img)
                cv2.imshow(hoststr, img)
                print (left_distance, right_distance)
                #csv_writer.write_data(f, left_distance, right_distance, front, left, right) #creating dataset
                if cv2.waitKey(1) == 27:
                    exit(0)


def run_camera():
    camera = Camera()
    camera.stream()


def control():
    car = controller.CarController()
    car.control_car()


def main():
    pool = Pool(processes=2)
    pool.apply_async(control)
    pool.apply_async(run_camera)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
