import math
from Vector import Vector
from Particle import Particle
from Physics import *


class Attractor(Particle):
    def __init__(self, state, position, momentum):
        Particle.__init__(self, state, position, momentum)
        self.values.set('ignoreDrag', True)
        self.values.set('ignoreGravity', True)
        self.values.add('attraction', 300)
        self.physicsName = 'attractors'
        self.name = 'attractor'

