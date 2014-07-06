from Vector import Vector

class Particle:
    def __init__(self, position, momentum):
        self.lifeTime = 0
        self.momentum = momentum
        self.position = position
        self.unattractable = False
        self.ignoreGravity = False
        self.destroyOnCollision = False
