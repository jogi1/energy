import sys
from Vector import Vector
from Helper import limit

class Camera:
    def __init__(self, state):
        self.position = Vector(0, 0, 100)
        self.orientation = Vector(0, 0, 0)
        self.frame = 0
        self.dirty = False
        self.directionVectors = self.orientation.getDirectionVectors()
        self.state = state
        self.read_config()

    def read_config(self):
        self.sensitivity = self.state.config['camera']['sensitivity']
        self.z_speed = self.state.config['camera']['z_speed'] * self.sensitivity
        self.movement_speed = self.state.config['camera']['movement_speed'] * self.sensitivity
        self.yaw_speed = self.state.config['camera']['sensitivity_3d']['yaw'] * self.sensitivity
        self.pitch_speed = self.state.config['camera']['sensitivity_3d']['pitch'] * self.sensitivity

    def up(self):
        self.position.z -= self.z_speed

    def down(self):
        self.position.z += self.z_speed

    def forward(self):
        dir = self.getDirectionVectors()
        v = dir.forward.scale(self.movement_speed, True)
        v.z = 0
        self.position -= v

    def back(self):
        dir = self.getDirectionVectors()
        v = dir.forward.scale(self.movement_speed, True)
        v.z = 0
        self.position += v

    def left(self):
        dir = self.getDirectionVectors()
        self.position += dir.right.scale(self.movement_speed, True)

    def right(self):
        dir = self.getDirectionVectors()
        self.position -= dir.right.scale(self.movement_speed, True)

    def rotate_yaw(self, distance):
        self.orientation.y -= distance * self.yaw_speed
        if self.orientation.y < 0:
            self.orientation.y += 360
        if self.orientation.y > 360:
            self.orientation.y -= 360
        self.dirty = True

    def rotate_pitch(self, distance):
        self.dirty = True
        self.orientation.x += distance * self.pitch_speed
        self.orientation.x = limit(self.orientation.x, -90, 90)

    def getDirectionVectors(self):
        if self.dirty:
            self.directionVectors = self.orientation.getDirectionVectors()
            self.dirty = False
        return self.directionVectors



