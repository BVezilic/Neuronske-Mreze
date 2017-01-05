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
        self.command = [0, 0, 0, 0]

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

    def control(self, cmd):
        if round(cmd[0]) == 1:
            self.forward()
        else:
            self.forward_stop()
        if round(cmd[1]) == 1:
            self.left()
        else:
            self.left_stop()
        if round(cmd[2]) == 1:
            self.right()
        else:
            self.right_stop()

    def keyup(self, e):
        if e.char == 'w' or e.char == 'W':
            self.command[0] = 0
            self.forward_stop()
        if e.char == 'a' or e.char == 'A':
            self.command[1] = 0
            self.left_stop()
        if e.char == 'd' or e.char == 'D':
            self.command[2] = 0
            self.right_stop()
        if e.char == 's' or e.char == 'S':
            self.command[3] = 0
            self.backward_stop()
        print self.command

    def keydown(self, e):
        if e.char == 'w' or e.char == 'W':
            self.command[0] = 1
            self.forward()
        if e.char == 'a' or e.char == 'A':
            self.command[1] = 1
            self.left()
        if e.char == 'd' or e.char == 'D':
            self.command[2] = 1
            self.right()
        if e.char == 's' or e.char == 'S':
            self.command[3] = 1
            self.backward()
        print self.command

    def control_car(self):
        root = Tk()
        frame = Frame(root, width=0, height=0)
        frame.bind("<KeyPress>", self.keydown, self)
        frame.bind("<KeyRelease>", self.keyup, self)
        frame.pack()
        frame.focus_set()
        root.mainloop()

#car = CarController()
#car.control_car()


