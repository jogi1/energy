

class Spawner:
    def __init__(self, state, delay):
        self.state = state
        self.delay = delay
        self.lastSpawntime = 0

    def spawn(self):
        if self.state.currentTime - self.lastSpawntime < self.delay:
            return False
        self.lastSpawntime = self.state.currentTime
        return True
