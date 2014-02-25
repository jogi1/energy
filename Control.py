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
        self.mousebuttons = [False, False, False, False ,False, False]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mousebuttons[event.button] = True

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
        if self.pressed[K_s]:
            self.state.camera.back()
        if self.pressed[K_a]:
            self.state.camera.left()
        if self.pressed[K_d]:
            self.state.camera.right()
        if self.mousebuttons[5] or self.pressed[K_e]:
            self.state.camera.down()
        if self.mousebuttons[4] or self.pressed[K_q]:
            self.state.camera.up()

        if self.state.block_cursor:
            self.state.camera.rotate_pitch(relative[1])
            self.state.camera.rotate_yaw(relative[0])
        else:
            self.state.mouse.frame(relative)

