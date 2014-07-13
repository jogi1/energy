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
from Timebubble import Timebubble
from Particle import Particle
from Spawner import Spawner
from Weapon import *

from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def renderCircle(middle, radius, segments = 60):
    glBegin(GL_LINE_LOOP)
    for i in xrange(0, segments):
        theta = (2.0 * math.pi * i) / segments
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        glVertex3f(middle.x + x, middle.y + y, 0)
    glEnd()

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
    self.mouseAttractor = Attractor(self, Vector(), Vector())
    self.physics.registerAttractor(self.mouseAttractor)
    self.particleSpawnTime = time.time()
    self.attractorSpawnTime = time.time()
    self.timebubbleSpawnTime = time.time()
    for x in xrange(5000):
        p = Particle(self, Vector(random.randint(0, self.width), random.randint(0, self.height), 0), Vector())

def myControlFunc(state):
    state.mouseAttractor.position.x = state.mouse.screen_position.x
    state.mouseAttractor.position.y = state.mouse.screen_position.y
    return

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
    # timebubble
    glColor3f(0, 1, 1)
    for part in state.physics.timebubbles:
        glVertex3f(part.position.x, part.position.y, 0)
    glEnd();
    # render timebubbles circle
    glColor3f(0, 1, 1)
    for part in state.physics.timebubbles:
        renderCircle(part.position, part.timeRadius)

    glColor3f(0, 1, 0)
    for part in state.physics.attractors:
        renderCircle(part.position, part.attraction)

    glPointSize(1)
    glBegin(GL_POINTS)
    # particles
    for part in state.physics.particles:
        glColor3f((part.momentum.x +1)/10, (part.momentum.y +1)/10, 1)
        glVertex3f(part.position.x, part.position.y, 0)

    glEnd();


    glColor3f(1, 1, 1)
    if state.showHelp:
        state.render.drawTextblock((0, 16, 0), "F1 to toggle help\n1 to select particle gun\n2 to select attractor gun\n3 to select timebubble gun\nlmb -> shoot at cursor\nrmb -> spawn at cursor\nspace -> spawn at position")
    else:
        state.render.drawText((0, 16, 0), str(state.lastFrameTime))
        i = 0
        state.render.drawText((0, 32, 0), str(state.controls.selectWeapon['name']))
        for x in state.controls.selectWeapon['options']:
            state.render.drawText((0, 48 + i * 16, 0), x + ' ' + str(state.controls.selectWeapon['options'][x]))
            i = i + 1

    for part in state.physics.attractors:
        state.render.drawText(part.position.getTuplet(), str(part.attraction))
        if part.lifeTime is not 0:
            state.render.drawText((part.position.x, part.position.y +16, 0), str(part.getTimeToLife()))


class PyManMain:

    def respawnParticles(self):
        for x in xrange(5000):
            p = Particle(Vector(random.randint(0, self.width), random.randint(0, self.height), 0), Vector())
            self.physics.registerParticle(p)

    def spawnParticle(self):
        if not hasattr(self, 'particleWeapon'):
            self.particleWeapon = WeaponCursorAimed(self, 'Particle Cursor Aimed')
        self.particleWeapon.fire()

    def spawnAttractor(self, lifeTime = 3):
        if not hasattr(self, 'attractorSpawner'):
            self.attractorSpawner = Spawner(self, 0.5)
        if not self.attractorSpawner.spawn():
            return
        self.attractorSpawnTime = self.currentTime
        a = Attractor(self)
        a.lifeTime = lifeTime
        a.position = self.movement.position.clone()
        a.momentum = self.mouseAttractor.position - self.movement.position
        a.momentum = a.momentum.scale(0.1)
        a.attraction = self.pointerPull
        self.physics.registerAttractor(a)


    def spawnTimebubble(self, lifeTime = 3):
        if time.time() - self.timebubbleSpawnTime < 0.5:
            return
        self.timebubbleSpawnTime = time.time()
        t = Timebubble(self)
        t.position = self.mouse.screen_position
        self.physics.registerTimebubble(t)

    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""

    def __init__(self, width=1280 ,height=1024):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        self.currentTime = 0
        self.pygame = pygame
        self.config = Config.config
        self.fps = 60.0
        self.frametime = 1000.0/self.fps
        self.gametimeScale = 20
        self.showHelp = True
        """Set the window Size"""
        self.width = width
        self.height = height
        self.position = Vector(0, 0, 0)
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
