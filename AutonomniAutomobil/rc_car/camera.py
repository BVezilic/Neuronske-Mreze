# Author: Nina Marjanovic
# Description: Streams video using IP Webcam Android application

#Start app>Start server>Run script
#Press Esc to stop the script

from __future__ import print_function
import numpy as np
import cv2
import urllib2
from util import csv_writer
from ann import rnn
import lane_detector as fl
from simulator.simulator import Simulator
import controller
from multiprocessing import Pool


class Camera(object):
    def __init__(self, host='192.168.1.3:8080'):
        self.host = host
        #self.simulator = Simulator()
        self.car_controller = controller.CarController()

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
                genome = rnn.load_genome("../ann/winner_net")
                output = rnn.get_output(genome, [left_distance, right_distance])
                self.car_controller.control(output)
                print (output)
                #csv_writer.write_data(f, left_distance, right_distance) #creating dataset
                if cv2.waitKey(1) == 27:
                    f.close()
                    exit(0)


camera = Camera()
camera.stream()

"""
def run_camera():
    camera.stream()


def simulation():
    camera.simulator.simulate()


def main():
    run_camera()
    pool = Pool(processes=2)
    pool.apply_async(run_camera)
    pool.apply_async(simulation)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
"""
