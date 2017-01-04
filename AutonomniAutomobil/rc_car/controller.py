#Author: Nina Marjanovic
#Description: Controls RC car using keyboard


#1. Connect arduino (COM5 port)
#2. Run this script
#3. Use WASD to move car

import serial
from Tkinter import *


class CarController(object):

    def __init__(self, usb_port='COM5'):
        ser = serial.Serial(usb_port, 9600)
        self.ser = ser

    def forward(self):
        self.ser.write('0')    #Forward High

    def forward_stop(self):
        self.ser.write("1")    #Forward Low

    def backward(self):
        self.ser.write('2')    #Backward High

    def backward_stop(self):
        self.ser.write('3')    #Backward Low

    def left(self):
        self.ser.write("4")    #Left High

    def left_stop(self):
        self.ser.write("5")    #Left Low

    def right(self):
        self.ser.write("6")    #Right High

    def right_stop(self):
        self.ser.write("7")    #Right Low



car = CarController()
command = [0, 0, 0, 0]


def keyup(e):
    if e.char == 'w' or e.char == 'W':
        command[0] = 0
        car.forward_stop()
    if e.char == 'a' or e.char == 'A':
        command[1] = 0
        car.left_stop()
    if e.char == 'd' or e.char == 'D':
        command[2] = 0
        car.right_stop()
    if e.char == 's' or e.char == 'S':
        command[3] = 0
        car.backward_stop()
    print command

def keydown(e):
    if e.char == 'w' or e.char == 'W':
        command[0] = 1
        car.forward()
    if e.char == 'a' or e.char == 'A':
        command[1] = 1
        car.left()
    if e.char == 'd' or e.char == 'D':
        command[2] = 1
        car.right()
    if e.char == 's' or e.char == 'S':
        command[3] = 1
        car.backward()
    print command


def control_car():
    root = Tk()
    frame = Frame(root, width=0, height=0)
    frame.bind("<KeyPress>", keydown, car)
    frame.bind("<KeyRelease>", keyup, car)
    frame.pack()
    frame.focus_set()
    root.mainloop()

control_car()


