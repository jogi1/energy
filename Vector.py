import math

class DirectionVector:
    def __init__(self, forward, right, up):
        self.forward = forward
        self.right = right
        self.up = up
    def __str__(self):
        return "Direction Vector forward(%s) right(%s) up(%s)" % (self.forward, self.right, self.up)

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Vector (%d, %d, %d)" % (self.x, self.y, self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return Vector(self.x * other.x, self.y * other.y, self.z * other.z)

    def length(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    def scale(self, scale, return_new = False):
        if return_new:
            return Vector(self.x * scale, self.y * scale, self.z * scale)
        self.x *= scale
        self.y *= scale
        self.z *= scale
        return self

    def getTuplet(self):
        return [self.x, self.y, self.z]

    def clone(self):
        return Vector(self.x, self.y, self.z)

    def normalize(self):
        length = self.length()
        if length == 0:
            self.x = self.y = self.z = 0
            return self
        self.x /= length
        self.y /= length
        self.z /= length
        return self


    def getDirectionVectors(self):
        PITCH = 0
        YAW = 1
        ROLL = 2
        if self.y:
            angle = math.radians(self.y)
            sy = math.sin(angle)
            cy = math.cos(angle)
        else:
            sy = 0
            cy = 1

        if self.x:
            angle = math.radians(self.x)
            sp = math.sin(angle)
            cp = math.cos(angle)
        else:
            sp = 0
            cp = 1

        forward = Vector(cp * cy, cp * sy, -sp)

        if self.z:
            angle = math.radians(self.z)
            sr = math.sin(angle)
            cr = math.cos(angle)

            t = sr * sp;
            right = Vector(-1 * t * cy + cr * sy, -1 * t * sy - cr * cy, -1 * sr * cp)
            t = cr * sp
            up = Vector(t * cy + sr * sy, t * sy - sr * cy, cr * cp)
        else:
            right = Vector(sy, -cy , 0)
            up = Vector(sp * cy, sp * sy, cp)
        return DirectionVector(forward, right, up)
