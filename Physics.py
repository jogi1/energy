import math

class Physics:
    def __init__(self, state):
        self.attractors = []
        self.particles = []
        self.gravity = 0.098
        self.state = state

    def clearParticles(self):
        self.particles = []

    def clearAttractors(self):
        self.attractors = []

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

    def frame(self):
        if len(self.attractors):
            self.attractors[0].handle()
        for attractor in self.attractors:
            self.PhysicsGravity(attractor)
            for attracted in self.attractors:
                if attracted == attractor:
                    continue
                self.PhysicsAttraction(attractor, attracted)
            for particle in self.particles:
                self.PhysicsAttraction(attractor, particle)

        for attractor in self.attractors:
            self.PhysicsApplyMomentum(attractor)
            self.PhyicsScreenCollision(attractor)
        for particle in self.particles:
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
        if particle.ignoreGravity:
            return
        particle.momentum.y = particle.momentum.y + self.gravity

    def PhysicsApplyMomentum(self, particle):
        particle.position = particle.position + particle.momentum.scale(10 * self.state.lastFrameTime, True)

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

