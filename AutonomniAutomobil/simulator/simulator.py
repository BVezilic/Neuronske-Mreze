import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Simulator:

    def __init__(self):
        self.left_lane = [(0, 0), (0,0)]
        self.right_lane = [(0, 0), (0,0)]
        self.left_distance = 0
        self.right_distance = 0

    def set_params(self, left_lane, right_lane, left_distance, right_distance):
        self.left_lane = left_lane
        self.right_lane = right_lane
        self.left_distance = left_distance
        self.right_distance = right_distance
        print self.left_lane

    def draw_lines(self):
        glBegin(GL_LINES)
        #if self.left_lane is not False:
         #   print self.left_lane[0]
        #line1
        '''
        glVertex2d(line1[0], line1[1])  #vertex1: x, y
        glVertex2d(line1[2], line1[3])  #vertex2: x, y
        #line2
        glVertex2d(line2[0], line2[1])  # vertex1: x, y
        glVertex2d(line2[2], line2[3])  # vertex2: x, y
        glEnd()
        '''

    @staticmethod
    def draw_car():
        glRectd(-0.1, -0.1, 0.1, 0.1)

    def simulate(self):
        pygame.init()
        display = (600, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -5)

        translate = 0
        rotate = 0
        while True:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glPushMatrix()
            self.draw_lines()
            glPopMatrix()
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                translate += 0.01
            if keys[K_a]:
                rotate += 1
            if keys[K_s]:
                translate -= 0.01
            if keys[K_d]:
                rotate -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glPushMatrix()
            glTranslated(0, translate, 0)
            glRotated(rotate, 0, 0, 1)

            self.draw_car()
            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(10)

