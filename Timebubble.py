
import math
from Vector import Vector
from Particle import Particle
from Physics import *

class Timebubble(Particle):
    def __init__(self, state, position, momentum):
        Particle.__init__(self, state, position, momentum)
        self.values.set('ignoreGravity', True)
        self.values.set('ignoreDrag',  True)
        self.values.set('unattractable', True)
        self.values.add('timeScale', 0.01)
        self.values.add('timeRadius', 200)
        self.timeRadius = 200
        self.physicsName = 'timebubbles'
        self.name = 'timebubble'

