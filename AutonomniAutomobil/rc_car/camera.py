# Author: Nina Marjanovic
# Description: Streams video using IP Webcam Android application

#Start app>Start server>Run script
#Press Esc to stop the script

from __future__ import print_function
import numpy as np
import cv2
import urllib2
#from ann import rnn
#import lane_detector as fl
import object_detection.sign_detection as sd
#import object_detection.car_detection as cd

#import controller


class Camera(object):
    def __init__(self, host='192.168.1.7:8080'):
        self.host = host
        #self.car_controller = controller.CarController()

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
                # img, left_distance, right_distance,  left_line, right_line = fl.detect_lanes(img)
                img = sd.detect_focal(img)
                #img = cd.select_roi(img)
                cv2.imshow(hoststr, img)
                # genome = rnn.load_genome("../ann/winner_net")
                # output = rnn.get_output(genome, [left_distance, right_distance])
                # self.car_controller.control(output)
                # print (output)
                if cv2.waitKey(1) == 27:
                    f.close()
                    exit(0)


camera = Camera()
camera.stream()
