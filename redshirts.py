#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

import array
import math
import random
import time

#import cairo
from Vector import Vector
from Mouse import Mouse
from Control import Control
from Camera import Camera
from Config import Config
from Render import Render
#from World import World
from Movement import Movement
from Physics import Physics
from Attractor import Attractor
from Particle import Particle
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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

def myInit(self):
    self.mouseAttractor = Attractor(self)
    self.physics.registerAttractor(self.mouseAttractor)
    self.particleSpawnTime = time.time()
    self.attractorSpawnTime = time.time()
    for x in xrange(5000):
        p = Particle(Vector(random.randint(0, self.width), random.randint(0, self.height), 0), Vector())
        self.physics.registerParticle(p)

def myControlFunc(state):
    state.mouseAttractor.position.x = state.mouse.screen_position.x
    state.mouseAttractor.position.y = state.mouse.screen_position.y
    if state.controls.mousebuttons[1]:
        state.mouseAttractor.attraction = state.pointerPull
    else:
        state.mouseAttractor.attraction = 0


def my2Dfunc(state):
    glPointSize(3)
    glBegin(GL_POINTS)
    glColor3f(1, 0, 0)
    # position
    glVertex3f(state.movement.position.x, state.movement.position.y, 0);
    glColor3f(1, 1, 1)
    # pointer
    glVertex3f(state.mouse.screen_position.x, state.mouse.screen_position.y, 0);
    # attractors
    glColor3f(0, 1, 0)
    for part in state.physics.attractors:
        glVertex3f(part.position.x, part.position.y, 0)
    glEnd();
    glPointSize(1)
    glBegin(GL_POINTS)
    # particles
    for part in state.physics.particles:
        glColor3f((part.momentum.x +1)/10, (part.momentum.y +1)/10, 1)
        glVertex3f(part.position.x, part.position.y, 0)

    glEnd();
    glColor3f(1, 1, 1)
    state.render.drawText((0, 16, 0), str(state.lastFrameTime))
    state.render.drawText((0, 32, 0), str(state.movement.position))
    state.render.drawText((0, 64, 0), str(state.controls.attractorTime if state.controls.attractorTime == 0 else (state.currentTime - state.controls.attractorTime) *2 ))

class PyManMain:

    def respawnParticles(self):
        for x in xrange(5000):
            p = Particle(Vector(random.randint(0, self.width), random.randint(0, self.height), 0), Vector())
            self.physics.registerParticle(p)

    def spawnParticle(self):
        if time.time() - self.particleSpawnTime < 0.01:
            return
        self.particleSpawnTime = time.time()
        position = self.movement.position.clone()
        momentum = self.mouseAttractor.position - self.movement.position
        momentum = momentum.scale(0.1)
        a = Particle(position, momentum)
        self.physics.registerParticle(a)

    def spawnAttractor(self, lifeTime = 3):
        if time.time() - self.attractorSpawnTime < 0.5:
            return
        self.attractorSpawnTime = time.time()
        a = Attractor(self)
        a.lifeTime = lifeTime
        a.position = self.movement.position.clone()
        a.momentum = self.mouseAttractor.position - self.movement.position
        a.momentum = a.momentum.scale(0.1)
        self.physics.registerAttractor(a)

    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""

    def __init__(self, width=1280 ,height=1024):
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
        self.movement = Movement(self)
        #self.world = World()
        self.physics = Physics(self)
        self.fps_clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        #self.cursor = TextureLoad('cursor')
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.currentTime = time.time()

        myInit(self)

        self.render.register2dFunction(my2Dfunc)
        self.render.disable3D = True
        self.lastFrameTime = 0
        self.pointerPull = 300

        def MainLoop(self):
            """This is the Main Loop of the Game"""
        while 1:
            self.currentTime = time.time()
            self.controls.pre_event()
            myControlFunc(self)
            self.physics.frame()
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

            self.fps_clock.tick(60)
            self.lastFrameTime = time.time() - self.currentTime


if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
