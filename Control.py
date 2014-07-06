from Vector import Vector
from pygame.locals import *
import pygame

class Control:
    def __init__(self, state):
        self.state = state
        self.pressed = []
        self.pressed_last_frame = []
        self.mousebuttons = [False, False, False, False ,False, False]

    def pre_event(self):
        return
        self.mousebuttons = [False, False, False, False ,False, False]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mousebuttons[event.button] = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mousebuttons[event.button] = False

    def frame(self):
        self.pressed_last_frame = self.pressed
        self.pressed = self.state.pygame.key.get_pressed()
        relative = self.state.pygame.mouse.get_rel()

        if self.pressed[K_LCTRL]:
            self.state.block_cursor = True
        else:
            self.state.block_cursor = False

        if self.pressed[K_w]:
            self.state.camera.forward()
            self.state.movement.up()
        if self.pressed[K_s]:
            self.state.camera.back()
            self.state.movement.down()
        if self.pressed[K_a]:
            self.state.camera.left()
            self.state.movement.left()
        if self.pressed[K_d]:
            self.state.movement.right()
            self.state.camera.right()
        if self.mousebuttons[5] or self.pressed[K_e]:
            self.state.pointerPull = self.state.pointerPull + 10
            self.state.camera.down()
            print self.state.pointerPull
        if self.mousebuttons[4] or self.pressed[K_q]:
            self.state.pointerPull = self.state.pointerPull - 10
            print self.state.pointerPull
            self.state.camera.up()
        if self.pressed[K_t]:
            self.state.physics.clearAttractors()
        if self.pressed[K_y]:
            self.state.physics.clearParticles()

        if self.pressed[K_SPACE]:
            self.state.spawnParticle()

        if self.mousebuttons[3]:
            self.state.spawnAttractor()

        if self.state.block_cursor:
            self.state.camera.rotate_pitch(relative[1])
            self.state.camera.rotate_yaw(relative[0])
        else:
            self.state.mouse.frame(relative)

