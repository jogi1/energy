import pygame
import math
import sys
import time

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from plane import isect_line_plane_v3

from Vector import Vector

from noise import pnoise2, snoise2

from PIL import Image

class World:
    def __init__(self, state, size=(128, 128), octaves=1):
        start = time.clock()
        self.freq = 16.0 * octaves
        self.size = size
        self.octaves = octaves
        self.state = state
        self.tiles = np.zeros((state.width, state.height, 3))
        self.texture = None
        self.createWorldTexture()

        return
        for x in range(size[0]):
            for y in range(size[1]):
                self.volume[x][y] = int(snoise2(x / self.freq, y / self.freq, self.octaves) * 127.0 + 128.0)

    def getWorldData(self):
        tmp = []
        width = 1280
        height = 1280
        for x in range(height):
            for y in range(width):
                if x < height * .5 and y < width* 0.5:
                #if y % 2 == 0:
                    tmp.append(chr(24))
                    tmp.append(chr(128))
                    tmp.append(chr(24))
                    tmp.append(chr(255))
                elif x > height * .5 and y < width* 0.5:
                    tmp.append(chr(24))
                    tmp.append(chr(24))
                    tmp.append(chr(128))
                    tmp.append(chr(255))
                elif x > height * .5 and y > width* 0.5:
                    tmp.append(chr(128))
                    tmp.append(chr(24))
                    tmp.append(chr(24))
                    tmp.append(chr(255))
                else:
                    tmp.append(chr(0))
                    tmp.append(chr(0))
                    tmp.append(chr(0))
                    tmp.append(chr(255))
        return ''.join(ss for ss in tmp)


    def createWorldTexture(self):
        width = 1280
        height = 1280
        return
    
        img = Image.frombuffer("RGBA", (width, height), self.getWorldData()) 
        img.save('testfile.jpeg')
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.getWorldData())

    def draw(self, state):
        if self.texture:
            glBindTexture( GL_TEXTURE_2D, self.texture )
            glBegin(GL_QUADS)
            #glColor3f(1, 0, 0)
            glTexCoord2f(0,0)
            glVertex2f(0,0)

            #glColor3f(0, 1, 0)
            glTexCoord2f(1, 0)
            glVertex2f( self.state.width, 0)

            #glColor3f(0, 0, 1)
            glTexCoord2f(1, 1)
            glVertex2f( self.state.width, self.state.height)

            #glColor3f(0, 1, 1)
            glTexCoord2f(0, 1)
            glVertex2f(0, self.state.height)
            glEnd()
            glBindTexture( GL_TEXTURE_2D, 0)

        return
        offset = (400, 400, 0)
        for x in xrange(1, self.size[0] -1):
            for y in xrange(1, self.size[1] -1):
                self.state.render.drawText((x*16, y*16, 0), str(self.volume[x][y]))


