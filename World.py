import pygame
import math
import sys
import time

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from plane import isect_line_plane_v3

from Noise import Noise
from Vector import Vector

class World:
    def __init__(self, size=(12, 12, 12)):
        start = time.clock()
        self.size = size
        self.volume = np.zeros(size)
        self.Noise = Noise()
        for x in range(1, size[0]-1):
            start_x = time.clock()
            for y in range(1, size[1]-1):
                for z in range(1, size[2]-1):
                    xf = float(float(x)/float(size[0]))
                    yf = float(y)/float(size[1])
                    zf = float(z)/float(size[2])
                    value = self.Noise.simplex(1, Vector(xf*3, yf*3, zf*3))
                    #print "(%f) (%f) (%f) - %f)" % (xf, yf, zf, value)
                    self.volume[x][y][z] = value
            print "x finished in %f" % (time.clock() - start_x)
        print "finixed in %f" % (time.clock() - start)


