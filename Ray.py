from Vector import Vector
from Options import Options

from OpenGL.GL import *
from OpenGL.GLU import *

class Ray(object):

    allRays = []

    def __init__(self, state, position=Vector(0, 0, 0), momentum=Vector(0, 0, 0), color=(1, 0, 0, 0.5)):
        self.spawnTime = state.currentTime
        self.state = state
        self.lifetime = 0
        self.position = position
        self.momentum = momentum
        self.values = Options()
        self.values.add('unattractable', False)
        self.values.add('ignoreGravity', False)
        self.values.add('ignoreDrag', False)
        self.physicsName = 'ray'
        self.color = color

    def __getattr__(self, key):
        return self.values.get(key)

    def spawn(self):
        list = getattr(self.state.physics, self.physicsName)
        list.append(self)
        allRays.append(self)

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

    def drawAll(self):
        for ray in self.allRays:
            ray.draw()

    def draw(self):
        tics = 300
        position = self.position
        self.momentum.scale(0.1)

        glColor4f(*self.color)
        glBegin(GL_LINE_STRIP)
        glVertex3f(*position.getTuplet())
        for x in range(tics):
            timescale = self.state.gametimeScale
            self.state.physics.PhysicsGravity(self)
            for attractor in self.state.physics.attractors:
                self.state.physics.PhysicsAttraction(attractor, self)
            self.state.physics.PhysicsApplyMomentum(self)
            position = position + self.momentum.scale(timescale *  1/self.state.fps, True)
            glVertex3f(*position.getTuplet())

        glEnd()
