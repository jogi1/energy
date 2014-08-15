import math
from Helper import limit

class Physics:
    def __init__(self, state):
        self.attractors = []
        self.particles = []
        self.timebubbles = []
        self.gravity = 0.2
        self.state = state

    def clearParticles(self):
        self.particles = []

    def clearAttractors(self):
        self.attractors = []

    def clearTimebubbles(self):
        self.timebubbles = []

    def registerParticle(self, particle):
        if isinstance(particle, list):
            self.particles = self.particles + particle
        else:
            self.particles.append(particle)

    def registerAttractor(self, attractor):
        if isinstance(attractor, list):
            self.attractors = self.attractors + attractor
        else:
            self.attractors.append(attractor)

    def registerTimebubble(self, timebubble):
        if isinstance(timebubble, list):
            self.timebubbles = self.timebubbles + timebubble
        else:
            self.timebubbles.append(timebubble)
        print len(self.timebubbles)

    def collideScreen(self, position):
        position.x = limit(position.x, 0, self.state.width)
        position.y = limit(position.y, 0, self.state.height)

    def handleMovement(self):
        self.state.movement.momentum.x = limit(self.state.movement.momentum.x, -10, 10)
        self.state.movement.momentum.y = limit(self.state.movement.momentum.y, -10, 10)
        self.PhysicsGravity(self.state.movement)
        self.state.movement.position = self.state.movement.position + self.state.movement.momentum.scale(self.state.gametimeScale * self.state.lastFrameTime, True)
        self.collideScreen(self.state.movement.position)


    def frame(self):
        self.handleMovement()
        if len(self.attractors):
            self.attractors[0].handle()
        for attractor in self.attractors:
            for attracted in self.attractors:
                if attracted == attractor:
                    continue
                self.PhysicsAttraction(attractor, attracted)
            for particle in self.particles:
                self.PhysicsAttraction(attractor, particle)

            for particle in self.timebubbles:
                self.PhysicsAttraction(attractor, particle)

        for attractor in self.attractors:
            self.PhysicsGravity(attractor)
            self.PhysicsApplyMomentum(attractor)
            self.PhyicsScreenCollision(attractor)

        for particle in self.particles:
            self.PhysicsGravity(particle)
            self.PhysicsApplyMomentum(particle)
            self.PhyicsScreenCollision(particle)

        for particle in self.timebubbles:
            self.PhysicsGravity(particle)
            self.PhysicsApplyMomentum(particle)
            self.PhyicsScreenCollision(particle)

    def PhysicsAttraction(state, attractor, particle):
        # apply attraction
        if attractor.attraction == 0 or particle.unattractable:
            return
        d = attractor.position - particle.position
        if d.length() <= attractor.attraction:
            particle.momentum = particle.momentum + d.scale((1/(math.fabs(particle.position.x) + math.fabs(particle.position.y)+1) * (attractor.attraction*3/(d.length()+0.001))))

    def PhysicsGravity(self, particle):
        # apply gravity
        if not particle.ignoreGravity:
            particle.momentum.y = particle.momentum.y + self.gravity
        # apply drag
        if not particle.ignoreDrag:
            particle.momentum = particle.momentum.scale(.99)

    def PhysicsApplyMomentum(self, particle):
        # apply time effects
        timescale = self.state.gametimeScale
        for timebubble in self.state.physics.timebubbles:
            d = particle.position - timebubble.position
            if d.length() <= timebubble.timeRadius:
                timescale = timescale * timebubble.timeScale
        particle.position = particle.position + particle.momentum.scale(timescale * 1/self.state.fps, True) #self.state.lastFrameTime, True)

    def PhyicsScreenCollision(self, particle):
        state = self.state
        if particle.position.y >= state.height:
            particle.position.y = state.height-1
            particle.momentum.y = 0
        if particle.position.y < 0:
            particle.position.y = 0
            particle.momentum.y = 0
        if particle.position.x >= state.width:
            particle.position.x = state.width-1
            particle.momentum.x = 0
        if particle.position.x < 0:
            particle.position.x = 0
            particle.momentum.x = 0

