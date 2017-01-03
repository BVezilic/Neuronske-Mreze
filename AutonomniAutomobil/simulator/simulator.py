#Author: Nina Marjanovic
#Description: Simulates road and vehicle in real time

#TODO get road data


import pygame
from pygame.locals import *
from OpenGL.GL import *


class Simulator(object):

    def __init__(self):
        self._left_lane = [(0, 0), (0, 0)]
        self._right_lane = [(0, 0), (0, 0)]
        self._left_distance = 0
        self._right_distance = 0

    @property
    def left_lane(self):
        return self._left_lane

    @left_lane.setter
    def set_left_lane(self, value):
        self._left_lane = value

    @property
    def right_lane(self):
        return self._right_lane

    @right_lane.setter
    def set_right_lane(self, value):
        self._right_lane = value

    @property
    def left_distance(self):
        return self._left_distance

    @left_distance.setter
    def set_left_distance(self, value):
        self._left_distance = value

    @property
    def right_distance(self):
        return self._right_distance

    @right_distance.setter
    def set_right_distance(self, value):
        self._right_distance = value

    def draw_lines(self):
        glBegin(GL_LINES)
        #line1
        if self.left_lane is not False:
            glVertex2d(self.left_lane[0][0], self.left_lane[0][1])  #vertex1: x, y
            glVertex2d(self.left_lane[1][0], self.left_lane[1][1])  #vertex2: x, y
        #line2
        if self.right_lane is not False:
            glVertex2d(self.right_lane[0][0], self.right_lane[0][1])  #vertex1: x, y
            glVertex2d(self.right_lane[1][0], self.right_lane[1][1])  #vertex2: x, y
        glEnd()


    @staticmethod
    def draw_car():
        glRectd(-0.1, -0.1, 0.1, 0.1)

    def simulate(self):
        pygame.init()
        width = 600
        height = 600
        display = (width, height)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)

        while True:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            glPushMatrix()
            self.draw_lines()
            glPopMatrix()

            glPushMatrix()
            self.draw_car()
            glPopMatrix()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


            pygame.display.flip()
            pygame.time.wait(10)


