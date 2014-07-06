from Vector import Vector
from Helper import limit

class Movement:
    def __init__(self, state):
        self.position = Vector()
        self.state = state
        self.speed = 100

    def collideScreen(self):
        self.position.x = limit(self.position.x, 0, self.state.width)
        self.position.y = limit(self.position.y, 0, self.state.height)

    def up(self):
        self.position.y = self.position.y - self.speed * self.state.lastFrameTime
        self.collideScreen()

    def down(self):
        self.position.y = self.position.y + self.speed * self.state.lastFrameTime
        self.collideScreen()

    def left(self):
        self.position.x = self.position.x - self.speed * self.state.lastFrameTime
        self.collideScreen()

    def right(self):
        self.position.x = self.position.x + self.speed * self.state.lastFrameTime
        self.collideScreen()

