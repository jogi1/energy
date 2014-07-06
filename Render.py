
import pygame
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from plane import isect_line_plane_v3

class Render:
    def __init__(self, state):
        self.state = state
        self.setup_window()
        self.disable2D = False;
        self.disable3D = False;
        self.functions2D = []


    def register2dFunction(self, function):
        self.functions2D.append(function)


    def drawText(self, position, textString):
        font = pygame.font.Font (None, 64)
        textSurface = font.render(textString, True, (255,255,255,255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glPushMatrix()
        glRasterPos3d(*position)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
        glPopMatrix()

    def renderGrid(self, grid_size=32):
        glColor3f(1, 1,  1)
        glLineWidth(1)
        grid_length = grid_size * 200;
        for x in range(-100, 100):
            glBegin(GL_LINES)
            glVertex3f(x * grid_size , -1 * grid_length, 0)
            glVertex3f(x * grid_size, 1 * grid_length, 0)
            glEnd()

        for x in range(-100, 100):
            glBegin(GL_LINES)
            glVertex3f(-1 * grid_length, x * grid_size, 0)
            glVertex3f(1 * grid_length, x * grid_size, 0)
            glEnd()

        glLineWidth(5)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(-1 * grid_length, 0, 0)
        glVertex3f(1 * grid_length, 0, 0)
        glEnd()

        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, -1 * grid_length, 0)
        glVertex3f(0, 1 * grid_length, 0)
        glEnd()

        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, -1 * grid_length)
        glVertex3f(0, 0, 1 * grid_length)
        glEnd()

    def setup_window(self):
        flag = OPENGL | DOUBLEBUF
        self.screen = pygame.display.set_mode((self.state.width, self.state.height), flag)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def setupFrustrum(self):
        ymax = 4 * math.tan(90 * math.pi / 360.0)
        ymin = -ymax;
        xmin = ymin * 4/3
        xmax = ymax * 4/3
        glFrustum(xmin, xmax, ymin, ymax, 4, 4096)

    def setup_3D(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.state.width, self.state.height)
        self.setupFrustrum()
        glMatrixMode (GL_MODELVIEW);
        glLoadIdentity()
        # the quake way
        glRotated(-90, 1, 0, 0)
        glRotated(90, 0, 0, 1)
        glRotated(-self.state.camera.orientation.z, 1, 0, 0)
        glRotated(-self.state.camera.orientation.x, 0, 1, 0)
        glRotated(-self.state.camera.orientation.y, 0, 0, 1)
        glTranslated(self.state.camera.position.x, self.state.camera.position.y, self.state.camera.position.z)

    def renderTouch(self):
        point = gluUnProject(self.state.mouse.screen_position.x, self.state.height - self.state.mouse.screen_position.y, 0)
        point1 = gluUnProject(self.state.mouse.screen_position.x, self.state.height - self.state.mouse.screen_position.y, 1)
        glColor(1, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(point[0], point[1], point[2])
        glVertex3f(point1[0], point1[1], point1[2])
        glEnd()

        p = isect_line_plane_v3(point, point1, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

        if p:
            glColor(1, 0, 1)
            glPointSize(2)
            glBegin(GL_POINTS)
            glVertex3f(p[0], p[1], p[2])
            glEnd()

            glColor(1, 1, 0)
            glBegin(GL_LINES)
            glVertex3f(p[0] - 16, p[1] - 16, p[2])
            glVertex3f(p[0] + 16, p[1] - 16, p[2])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(p[0] + 16, p[1] - 16, p[2])
            glVertex3f(p[0] + 16, p[1] + 16, p[2])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(p[0] + 16, p[1] + 16, p[2])
            glVertex3f(p[0] - 16, p[1] + 16, p[2])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(p[0] - 16, p[1] + 16, p[2])
            glVertex3f(p[0] - 16, p[1] - 16, p[2])
            glEnd()

    def render_3D(self):
        self.setup_3D()
        self.renderGrid()
        self.renderTouch()
        return

    def setup_2D(self):
        glViewport(0, 0, self.state.width, self.state.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.state.width, self.state.height, 0, -99999, 99999)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def render_2D(self):
        self.setup_2D()
        for x in self.functions2D:
            x(self.state)
        #self.drawText((320, 200, 0), "TEST")

    def frame(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
        if (not self.disable3D):
            self.render_3D()
        if (not self.disable2D):
            self.render_2D()

