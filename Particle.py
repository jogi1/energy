from Vector import Vector
from Options import Options

class Particle(object):
    def __init__(self, state, position=Vector(0, 0, 0), momentum=Vector(0, 0, 0)):
        self.spawnTime = state.currentTime
        self.state = state
        self.lifeTime = 0
        self.momentum = momentum
        self.position = position
        self.destroyOnCollision = False
        self.physicsName = 'particles'
        self.handlers = []
        self.addHandler(self.handleLifetime)
        self.name = 'particle'
        self.values = Options()
        self.values.add('unattractable', False)
        self.values.add('ignoreGravity', False)
        self.values.add('ignoreDrag', False)

    def __getattr__(self, key):
        return self.values.get(key)


    def spawn(self):
        list = getattr(self.state.physics, self.physicsName)
        list.append(self)

    def addHandler(self, handler):
        self.handlers.append(handler)

    def handleLifetime(self):
        parts = []
        cparts = getattr(self.state.physics, self.physicsName)
        for particle in cparts:
            if particle.lifeTime:
                if self.state.currentTime - particle.spawnTime > particle.lifeTime:
                    continue
            parts.append(particle)
        setattr(self.state.physics, self.physicsName, parts)

    def getTimeToLife(self):
        return self.lifeTime - (self.state.currentTime - self.spawnTime)

    def handle(self):
        for handler in self.handlers:
            handler()


