import math
from Vector import Vector
from Particle import Particle
from Physics import *


class Attractor(Particle):
    def __init__(self, state):
        Particle.__init__(self, Vector(), Vector())
        self.state = state
        self.spawnTime = state.currentTime
        self.lifeTime = 0
        self.attraction = 300
        self.ignoreGravity = True

    def handle(self):
        att = []
        for attractor in self.state.physics.attractors:
            if attractor.lifeTime:
                if self.state.currentTime - attractor.spawnTime > attractor.lifeTime:
                    continue
            att.append(attractor)
        self.state.physics.attractors = att


