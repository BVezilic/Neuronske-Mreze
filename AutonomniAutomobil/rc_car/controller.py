#Author: Nina Marjanovic
#Description: Controls RC car using keyboard

import serial
from msvcrt import getch

class CarController(object):

    def __init__(self, usb_port='COM5'):
        ser = serial.Serial(usb_port, 9600)
        self.ser = ser

    def forward(self):
        self.ser.write('H')    #Forward High

    def forward_stop(self):
        self.ser.write("FL")    #Forward Low

    def backward(self):
        self.ser.write('H')    #Backward High

    def backward_stop(self):
        self.ser.write('L')    #Backward Low

    def left(self):
        self.ser.write("LH")    #Left High

    def left_stop(self):
        self.ser.write("LL")    #Left Low

    def right(self):
        self.ser.write("RH")    #Right High

    def right(self):
        self.ser.write("RL")    #Right Low



#test

car = CarController()
while True:
    key = ord(getch())
    print (key)
    if key == 80:   #down
        car.backward()
    else:
        car.backward_stop()
