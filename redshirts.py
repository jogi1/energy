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

def add_v3v3(a, b):
    return [a[0] + b[0],
            a[1] + b[1],
            a[2] + b[2]]


def sub_v3v3(a, b):
    return [a[0] - b[0],
            a[1] - b[1],
            a[2] - b[2]]


def dot_v3v3(a, b):
    return (a[0] * b[0] +
            a[1] * b[1] +
            a[2] * b[2])


def mul_v3_fl(a, f):
    a[0] *= f
    a[1] *= f
    a[2] *= f


# intersection function
def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=0.000001):
    """
    p0, p1: define the line
    p_co, p_no: define the plane:
    p_co is a point on the plane (plane coordinate).
    p_no is a normal vector defining the plane direction; does not need to be normalized.

    return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    w = sub_v3v3(p0, p_co)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        fac = -dot_v3v3(p_no, w) / dot
        mul_v3_fl(u, fac)
        return add_v3v3(p0, u)
    else:
        return None

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

    def RenderGrid(self, grid_size=32):
        glColor3f(1, 1,  1)
        glLineWidth(1)
        grid_length = grid_size * 200;
        for x in range(-100, 100):
            glBegin(GL_LINES)
            glVertex3f(x * grid_size , -1 * grid_length, 0)
            glVertex3f(x * grid_size, 1 * grid_length, 0)
            glEnd()

        for x in range(-100, 100):
            glBegin(GL_LINES)
            glVertex3f(-1 * grid_length, x * grid_size, 0)
            glVertex3f(1 * grid_length, x * grid_size, 0)
            glEnd()

        glLineWidth(5)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(-1 * grid_length, 0, 0)
        glVertex3f(1 * grid_length, 0, 0)
        glEnd()

        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, -1 * grid_length, 0)
        glVertex3f(0, 1 * grid_length, 0)
        glEnd()

        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, -1 * grid_length)
        glVertex3f(0, 0, 1 * grid_length)
        glEnd()

    def setupFrustrum(self):
        ymax = 4 * math.tan(90 * math.pi / 360.0)
        ymin = -ymax;
        xmin = ymin * 4/3
        xmax = ymax * 4/3
        glFrustum(xmin, xmax, ymin, ymax, 4, 4096)

    def OpenglSetup3D(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        self.setupFrustrum()
        glMatrixMode (GL_MODELVIEW);
        glLoadIdentity()
        # the quake way
        glRotated(-90, 1, 0, 0)
        glRotated(90, 0, 0, 1)
        glRotated(-self.camera.orientation.z, 1, 0, 0)
        glRotated(-self.camera.orientation.x, 0, 1, 0)
        glRotated(-self.camera.orientation.y, 0, 0, 1)
        glTranslated(self.camera.position.x, self.camera.position.y, self.camera.position.z)

    def OpenglSetup2D(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -99999, 99999)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



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
        """Create the Screen"""
        flag = OPENGL | DOUBLEBUF
        self.screen = pygame.display.set_mode((self.width, self.height), flag)
        self.fps_clock = pygame.time.Clock()
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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

            print self.position
            print self.rotation
            label = self.font.render(str(p[0]) + " " + str(p[1]), 1, pygame.Color(1, 1, 1))
            drawText((0, 0, 0), "TEST");
            self.OpenglSetup3D()
            self.RenderGrid()

            point = gluUnProject(self.mouse.screen_position.x, self.height - self.mouse.screen_position.y, 0)
            print "point: " + str(point)
            point1 = gluUnProject(self.mouse.screen_position.x, self.height - self.mouse.screen_position.y, 1)
            print "point1: " + str(point1)
            glColor(1, 1, 0)
            glBegin(GL_LINES)
            glVertex3f(point[0], point[1], point[2])
            glVertex3f(point1[0], point1[1], point1[2])
            glEnd()

            p = isect_line_plane_v3(point, point1, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
            print "p: " + str(p)

            if p:
                glColor(1, 0, 1)
                glPointSize(2)
                glBegin(GL_POINTS)
                glVertex3f(p[0], p[1], p[2])
                glEnd()

                glColor(1, 1, 0)
                glBegin(GL_LINES)
                glVertex3f(p[0] - 16, p[1] - 16, p[2])
                glVertex3f(p[0] + 16, p[1] - 16, p[2])
                glEnd()

                glBegin(GL_LINES)
                glVertex3f(p[0] + 16, p[1] - 16, p[2])
                glVertex3f(p[0] + 16, p[1] + 16, p[2])
                glEnd()

                glBegin(GL_LINES)
                glVertex3f(p[0] + 16, p[1] + 16, p[2])
                glVertex3f(p[0] - 16, p[1] + 16, p[2])
                glEnd()

                glBegin(GL_LINES)
                glVertex3f(p[0] - 16, p[1] + 16, p[2])
                glVertex3f(p[0] - 16, p[1] - 16, p[2])
                glEnd()

            self.OpenglSetup2D()

            glColor(1, 0, 0)
            glBegin(GL_POINTS)
            glVertex3f(0, 0, 0)
            glEnd()

            glColor(0, 1, 0)
            glBegin(GL_POINTS)
            glVertex3f(640, 0, 0)
            glEnd()

            glColor(0, 0, 1)
            glBegin(GL_POINTS)
            glVertex3f(640, 480, 0)
            glEnd()

            glColor(0, 1, 1)
            glBegin(GL_POINTS)
            glVertex3f(0, 480, 0)
            glEnd()

            self.fps_clock.tick(60)


if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
