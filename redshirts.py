#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

import array
import math
import random

import cairo
import rsvg
from Vector import Vector
from Mouse import Mouse
from Control import Control
from Camera import Camera
from Config import Config
from Render import Render
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# generic math functions
def AngleVectors(angles):
    PITCH = 0
    YAW = 1
    ROLL = 2
    if angles[YAW]:
        angle = math.radians(angles[YAW])
        sy = math.sin(angle)
        cy = math.cos(angle)
    else:
        sy = 0
        cy = 1

    if angles[PITCH]:
        angle = math.radians(angles[PITCH])
        sp = math.sin(angle)
        cp = math.cos(angle)
    else:
        sp = 0
        cp = 1

    forward = [cp * cy, cp * sy, -sp]

    if angles[ROLL]:
        angle = math.radians(angles[ROLL])
        sr = math.sin(angle)
        cr = math.cos(angle)

        t = sr * sp;
        right = [-1 * t * cy + cr * sy, -1 * t * sy - cr * cy, -1 * sr * cp]
        t = cr * sp
        up = [ t * cy + sr * sy, t * sy - sr * cy, cr * cp ]
    else:
        right = [ sy, -cy , 0]
        up = [ sp * cy, sp * sy, cp ]
    return [forward, right, up]


def TextureLoad(name, path=['resources'], extension=".svg",  width=32, height=32):
    filename = os.path.join(os.path.join(*path), name) + extension
    data = array.array('c', chr(0) * width * height * 4)
    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, width, height, width * 4)
    svg = rsvg.Handle(file=filename)
    svg_width = svg.props.width
    svg_height = svg.props.height
    scale_width = float(width)/float(svg_width)
    scale_height = float(height)/float(svg_height)
    ctx = cairo.Context(surface)
    ctx.scale(scale_width, scale_height)
    svg.render_cairo(ctx)
    return pygame.image.frombuffer(data.tostring(), (width, height), "ARGB")

 
def drawText(position, textString):
    font = pygame.font.Font (None, 64)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def limit(var, min, max):
    print var
    if var < min:
        return min
    if var > max:
        return max
    return var



class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        self.pygame = pygame
        self.config = Config.config
        self.fps = 60.0
        self.frametime = 1000.0/self.fps
        """Set the window Size"""
        self.width = width
        self.height = height
        self.position = [0, 0, 0]
        self.rotation = Vector(0, 0, 0)
        self.controls = Control(self)
        self.mouse = Mouse(self)
        self.camera = Camera(self)
        self.render = Render(self)
        self.fps_clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.cursor = TextureLoad('cursor')
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        def MainLoop(self):
            """This is the Main Loop of the Game"""
        while 1:
            self.controls.pre_event()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
                    self.controls.handle_event(event)

            pygame.event.pump()
            pygame.display.flip()
            p = pygame.mouse.get_pos()
            self.controls.frame()

            if pygame.key.get_pressed()[K_x]:
                sys.exit()

            self.render.frame()

            print self.camera.position
            print self.camera.orientation

            self.fps_clock.tick(60)


if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
