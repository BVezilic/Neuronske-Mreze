# Author: Nina Marjanovic
# Description: Streams video using IP Webcam Android application, MAIN

#Start app>Start server>Run script
#Press Esc to stop the script

#from __future__ import print_function
import urllib2

import cv2
import numpy as np
import controller
import object_detection.lane_detector as fl
from ann.rnn import rnn
#from ann.cnn import cnn
from object_detection import tl_detection3 as tld
from object_detection import sign_detection as sd
import sklearn.preprocessing as sp


class Camera(object):
    def __init__(self, host='192.168.0.105:8080'):
        self.host = host
        self.car_controller = controller.CarController()

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
                img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
                # detect traffic light
                #tl_distance = tld.detect(img)[0]
                #print tl_distance
                # detect STOP sign
                #stop_distance, stop_img = sd.detect(img)
                # detect vehicle
                #is_vehicle = cnn.is_car(img.copy()[70:144, 20:156], cnn.get_model())
                # detect lanes
                img, left_distance, right_distance,  left_line, right_line = fl.detect_lanes(img)

                print left_distance
                print right_distance
                genome = rnn.load_genome("../ann/rnn/winner_net_left")
                # control
                data = [left_distance, right_distance]
                data_normalized = sp.normalize([data], norm='l2')
                output = rnn.get_output(genome, data_normalized[0])
                cv2.imshow(hoststr, img)
                self.car_controller.control(output)
                print (output)
                if cv2.waitKey(1) == 27:
                    exit(0)


camera = Camera()
camera.stream()
