#Author: Nina Marjanovic
#Description: Controls RC car using keyboard

import serial
from msvcrt import getch
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


def keyup(e):
    if e.char == 'w' or e.char == 'W':
        print 'stop up'
        car.forward_stop()
    if e.char == 'a' or e.char == 'A':
        print 'stop left'
        car.left_stop()
    if e.char == 'd' or e.char == 'D':
        print 'stop right'
        car.right_stop()
    if e.char == 's' or e.char == 'S':
        print 'stop down'
        car.backward_stop()


def keydown(e):
    if e.char == 'w' or e.char == 'W':
        print 'up'
        car.forward()
    if e.char == 'a' or e.char == 'A':
        print 'left'
        car.left()
    if e.char == 'd' or e.char == 'D':
        print 'right'
        car.right()
    if e.char == 's' or e.char == 'S':
        print 'down'
        car.backward()

root = Tk()
frame = Frame(root, width=0, height=0)
frame.bind("<KeyPress>", keydown, car)
frame.bind("<KeyRelease>", keyup, car)
frame.pack()
frame.focus_set()
root.mainloop()


