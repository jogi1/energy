from Helper import limit
from Vector import Vector
class Mouse:
    def __init__(self, state):
        self.screen_position = Vector(0, 0, 0)
        self.screen_position_lastframe = Vector(0, 0, 0)
        self.relative = Vector(0, 0, 0)
        self.state = state

    def frame(self, relative):
        self.relative.x, self.relative.y = relative
        self.screen_position_lastframe = self.screen_position
        self.screen_position += self.relative
        self.screen_position.x = limit(self.screen_position.x, 0, self.state.width)
        self.screen_position.y = limit(self.screen_position.y, 0, self.state.height)
