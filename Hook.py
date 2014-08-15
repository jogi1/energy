from Vector import Vector

class Hook:
    def __init__(self, state, anchorPoint):
        self.state = state
        self.anchorPoint = anchorPoint
        self.distance = (self.state.position - self.anchorPoint).distance()
        print distance

