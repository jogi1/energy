from Vector import Vector
from pygame.locals import *
from Timebubble import *
from Attractor import *
from Weapon import *
from Commands import *

import pygame


class Control:
    def __init__(self, state):
        self.commands = Commands(state)
        self.options = ['ignoreGravity', 'ignoreDrag', 'unattractable']
        self.particleWeapons = {
                'name': 'Particle',
                'aimed': WeaponCursorAimed(state, 'Particle Aimed', delay=0.01),
                'stationary': WeaponSpawnAtPosition(state, 'Particle stationary', delay=0.01),
                'cursor': WeaponSpawnAtCursor(state, 'Particle at cursor', delay=0.01),
                'options': Particle(state).values.getAllNameValue()
                }
        self.timeWeapons = {
                'name': 'Time',
                'aimed': WeaponSpawnAtCursor(state, 'Time Aimed', Timebubble),
                'stationary': WeaponSpawnAtPosition(state, 'Time stationary', Timebubble),
                'cursor': WeaponSpawnAtCursor(state, 'Time cursor', Timebubble),
                'options': Timebubble(state, Vector(), Vector()).values.getAllNameValue()
                }
        self.gravityWeapons = {
                'name': 'Attractor',
                'aimed': WeaponCursorAimed(state, 'Gravity Aimed', Attractor),
                'stationary': WeaponSpawnAtPosition(state, 'Gravity stationary', Attractor),
                'cursor': WeaponSpawnAtCursor(state, 'Gravity cursor', Attractor),
                'options': Attractor(state, Vector(), Vector()).values.getAllNameValue()
                }
        self.selectWeapon = self.particleWeapons
        self.state = state
        self.pressed = []
        self.pressed_last_frame = []
        self.mousebuttons = [False, False, False, False ,False, False]
        self.attractorTime = 0

        self.commands.register('toggleHelp', K_F1, {'start': self.toggleHelp})

    def pre_event(self):
        return
        self.mousebuttons = [False, False, False, False ,False, False]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mousebuttons[event.button] = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mousebuttons[event.button] = False

    def multiplyModificators(self, value):
        if self.pressed[K_LCTRL] and self.pressed[K_LSHIFT]:
            return value * 1000
        elif self.pressed[K_LCTRL]:
            return value * 100
        elif self.pressed[K_LSHIFT]:
            return value * 10
        return value

    def frame(self):
        self.pressed_last_frame = self.pressed
        self.pressed = self.state.pygame.key.get_pressed()
        relative = self.state.pygame.mouse.get_rel()

        self.commands.handle()

        if self.pressed[K_LCTRL]:
            self.state.block_cursor = True
        else:
            self.state.block_cursor = False

        for x in xrange(0, K_9 - K_0 + 1):
            if self.pressed[K_0 + x]:
                self.selectSlot(x)

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
            self.state.pointerPull = self.state.pointerPull + self.multiplyModificators(10)
        if self.mousebuttons[4] or self.pressed[K_q]:
            self.state.pointerPull = self.state.pointerPull - self.multiplyModificators(10)

        if self.pressed[K_t]:
            self.state.physics.clearAttractors()
        if self.pressed[K_y]:
            self.state.physics.clearParticles()
        if self.pressed[K_v]:
            self.state.physics.clearTimebubbles()

        if self.pressed[K_g]:
            self.state.gametimeScale = self.state.gametimeScale - self.multiplyModificators(0.05)
            if self.state.gametimeScale <= 0:
                self.state.gametimeScale = 0.05
        if self.pressed[K_h]:
            self.state.gametimeScale = self.state.gametimeScale + self.multiplyModificators(0.05)


        if self.state.block_cursor:
            self.state.camera.rotate_pitch(relative[1])
            self.state.camera.rotate_yaw(relative[0])
        else:
            self.state.mouse.frame(relative)

        if self.mousebuttons[1]:
            self.spawnSelectedAimed()

        if self.mousebuttons[3]:
            self.spawnSelectedCursor()

        if self.pressed[K_SPACE]:
            self.spawnSelectedStationary()

    def selectSlot(self, value):
        if value == 1:
            self.selectWeapon = self.particleWeapons
        if value == 2:
            self.selectWeapon = self.gravityWeapons
        if value == 3:
            self.selectWeapon = self.timeWeapons
        if value == 4:
            self.toggleOption('ignoreGravity')
        if value == 5:
            self.toggleOption('ignoreDrag')
        if value == 6:
            self.toggleOption('unattractable')

    def particleSetOptions(self, particle):
        for x in self.selectWeapon['options']:
            particle.values.set(x, self.selectWeapon['options'][x])

    def spawnSelectedAimed(self):
        self.selectWeapon['aimed'].fire()
        self.particleSetOptions(self.selectWeapon['aimed'].particle)

    def spawnSelectedStationary(self):
        self.selectWeapon['stationary'].fire()
        self.particleSetOptions(self.selectWeapon['stationary'].particle)

    def spawnSelectedCursor(self):
        self.selectWeapon['cursor'].fire()
        self.particleSetOptions(self.selectWeapon['cursor'].particle)

    def toggleOption(self, option):
        self.selectWeapon['options'][option] = not self.selectWeapon['options'][option]

    def toggleHelp(self):
        self.state.showHelp = not self.state.showHelp

