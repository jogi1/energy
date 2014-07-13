from Vector import Vector
from Helper import limit

class Movement:
    def __init__(self, state):
        self.ignoreGravity = False
        self.ignoreDrag = False
        self.position = Vector()
        self.momentum = Vector()
        self.state = state
        self.speed = 100

    def collideScreen(self):
        self.position.x = limit(self.position.x, 0, self.state.width)
        self.position.y = limit(self.position.y, 0, self.state.height)

    def down(self):
        return

    def up(self):
        self.momentum.y = self.momentum.y - self.speed * self.state.lastFrameTime

    def left(self):
        self.momentum.x = self.momentum.x - self.speed * self.state.lastFrameTime

    def right(self):
        self.momentum.x = self.momentum.x + self.speed * self.state.lastFrameTime

