
def add_v3v3(a, b):
    return [a[0] + b[0],
            a[1] + b[1],
            a[2] + b[2]]


def sub_v3v3(a, b):
    return [a[0] - b[0],
            a[1] - b[1],
            a[2] - b[2]]


def dot_v3v3(a, b):
    return (a[0] * b[0] +
            a[1] * b[1] +
            a[2] * b[2])


def mul_v3_fl(a, f):
    a[0] *= f
    a[1] *= f
    a[2] *= f


# intersection function
def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=0.000001):
    """
    p0, p1: define the line
    p_co, p_no: define the plane:
    p_co is a point on the plane (plane coordinate).
    p_no is a normal vector defining the plane direction; does not need to be normalized.

    return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    w = sub_v3v3(p0, p_co)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        fac = -dot_v3v3(p_no, w) / dot
        mul_v3_fl(u, fac)
        return add_v3v3(p0, u)
    else:
        return None
