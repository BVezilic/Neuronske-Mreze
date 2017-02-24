# Author: Nina Marjanovic
# Description: Streams video using IP Webcam Android application, MAIN
#              Uses RNN to control a RC car

#Start app>Start server>Run script
#Press Esc to stop the script

#from __future__ import print_function
import urllib2

import cv2
import numpy as np
import controller
import object_detection.lane_detector as fl
from ann.rnn import rnn
from ann.rnn import simple_rnn as sr
from ann.cnn import cnn
from object_detection import tl_detection3 as tld
from object_detection import sign_detection as sd
import sklearn.preprocessing as sp
import time


class Camera(object):
    def __init__(self, host='192.168.0.102:8080'):
        self.host = host
        self.car_controller = controller.CarController()
        self.rnn = sr.create_model()
        self.frame_counter = 0
        self.car_counter = 0
        self.rnn.load_weights("../ann/rnn/weights.h5")
        self.cnn = cnn.load_model('tezine.h5')
        self.detected_stop = False

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
                orig_img = img.copy()
                # increase frame_counter
                self.frame_counter += 1
                if self.frame_counter % 1 == 0:
                    # detect traffic light
                    tl_distance=-1#, img_tl = tld.detect(img)

                    # detect STOP sign
                    #if self.detected_stop is False:
                    stop_distance, img_stop = sd.detect(img)
                    orig_img = img_stop
                    print stop_distance

                    # detect vehicle [70:144, 20:156]
                    is_vehicle = cnn.is_car(img.copy()[70:144, 20:156], self.cnn)
                    #cv2.rectangle(img, (20, 70), (156, 144), (255, 0, 0))
                    #print "AUFTIC: " + str(is_vehicle)

                    if tl_distance != -1:
                        #self.car_controller.control([0.0, 0.0, 0.0])
                        print "TRAFFIC LIGHT - RED!"
                    if stop_distance != -1:
                        print "STOP"
                        start_time = time.time()
                        self.detected_stop = True
                        #while time.time() - start_time < 3:
                        self.car_controller.control([0.0, 0.0, 0.0])
                        #stop_distance = -1
                    if is_vehicle:
                        #print "VEHICLE DETECTED!"
                        self.car_counter += 1
                    if self.frame_counter % 5 == 0:
                        if self.car_counter >= 3:
                            pass#self.car_controller.control([0.0, 0.0, 0.0])
                        self.car_counter == 0

                    # detect lanes
                    img, left_distance, right_distance,  left_line, right_line = fl.detect_lanes(img)

                    #print left_distance
                    #print right_distance
                    # control
                    data = [left_distance, right_distance]
                    output = self.rnn.predict(np.expand_dims(np.array([data]),axis=0))
                    #print output
                    self.car_controller.control(output[0][0])
                    # reset frame_counter
                    self.frame_counter = 0
                    # merge with original image
                    #orig_img[64:, 0:] = img

                cv2.imshow(hoststr, orig_img)
                if cv2.waitKey(1) == 27:
                    exit(0)


camera = Camera()
camera.stream()
