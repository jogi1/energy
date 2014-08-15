from Vector import *
from Spawner import *
from Particle import *

class Weapon:
    def __init__(self, state, name, type=Particle, delay=0.1):
        self.name = name
        self.delay = delay
        self.spawner = Spawner(state, delay)
        self.type = type
        self.state = state
        self.values = Particle(state).values
        self.particle = None

    def fire(self, arguments):
        if not self.spawner.spawn():
            return
        self.particle = self.type(self.state, *arguments)
        self.particle.spawn()

class WeaponCursorAimed(Weapon, object):
    def __init__(self, state, name, type=Particle, delay=0.1):
        Weapon.__init__(self, state, name, type, delay)

    def fire(self):
        position = self.state.movement.position.clone()
        momentum = self.state.mouseAttractor.position - self.state.movement.position
        momentum = momentum.scale(0.1)
        super(WeaponCursorAimed, self).fire([position, momentum])

class WeaponSpawnAtPosition(Weapon, object):
    def __init__(self, state, name, type=Particle, delay=0.1):
        Weapon.__init__(self, state, name, type, delay)

    def fire(self):
        position = self.state.movement.position.clone()
        momentum = Vector(0, 0, 0)
        return super(WeaponSpawnAtPosition, self).fire([position, momentum])

class WeaponSpawnAtCursor(Weapon, object):
    def __init__(self, state, name, type=Particle, delay=0.1):
        Weapon.__init__(self, state, name, type, delay)

    def fire(self):
        position = self.state.mouseAttractor.position.clone()
        momentum = Vector(0, 0, 0)
        return super(WeaponSpawnAtCursor, self).fire([position, momentum])





