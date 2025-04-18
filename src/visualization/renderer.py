# src/visualization/renderer.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class Renderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.objects = []   # Lista de objetos (Line, Circle, Arc, etc.)
        self.mouse_down = False
        self.last_mouse_pos = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = 5.0     # Distancia inicial de la cámara
        self.show_grid = False
        self.grid_height = 0.0
        # Nuevo: tipo de plano para el grid: 0=XY, 1=YZ, 2=ZX
        self.grid_plane = 0
        self.grid_step = 1.0

    def initialize_window(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width / self.height), 0.1, 5000.0)  #Aumentar a 500 el parámetro soluciona el tema del zoom out

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.zoom)

        glLineWidth(2.0)
        print("Window initialized.")

    def update_scene(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up
                    self.zoom = max(1.0, self.zoom - 0.5)
                elif event.button == 5:  # Scroll down
                    self.zoom += 0.5
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
            elif event.type == MOUSEMOTION:
                if self.mouse_down:
                    x, y = pygame.mouse.get_pos()
                    dx = x - self.last_mouse_pos[0]
                    dy = y - self.last_mouse_pos[1]
                    self.rotation_x += dy * 0.5
                    self.rotation_y += dx * 0.5
                    self.last_mouse_pos = (x, y)
            elif event.type == KEYDOWN:
                if event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                    print("Grid toggled:", self.show_grid)
                elif event.key == pygame.K_UP:
                    self.grid_height += 0.5 - self.grid_height % 0.5
                    print("Grid height:", self.grid_height)
                elif event.key == pygame.K_DOWN:
                    self.grid_height -= (self.grid_height % 0.5) or 0.5
                    print("Grid height:", self.grid_height)
                elif event.key == pygame.K_LEFT:
                    self.grid_plane = (self.grid_plane - 1) % 3
                    print("Grid plane:", ["XY", "YZ", "ZX"][self.grid_plane])
                elif event.key == pygame.K_RIGHT:
                    self.grid_plane = (self.grid_plane + 1) % 3
                    print("Grid plane:", ["XY", "YZ", "ZX"][self.grid_plane])


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.zoom)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        self.draw_axes()
        if self.show_grid:
            self.draw_grid()

        for obj in self.objects:
            self.render_object(obj)

        pygame.display.flip()
        pygame.time.wait(10)

    def draw_axes(self):
        glLineWidth(2.0)
        glBegin(GL_LINES)
        # Eje X en rojo
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(2.0, 0.0, 0.0)
        # Eje Y en verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 2.0, 0.0)
        # Eje Z en azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 2.0)
        glEnd()

    def draw_grid(self):
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)
        # Extensión del grid
        grid_range = max(2.0, 2 * self.zoom)
        s = self.grid_step

        # Calculamos el límite inferior y superior alineado a múltiplos de 's'
        min_i = math.ceil(-grid_range / s) * s
        max_i = math.floor( grid_range / s) * s

        # Recorremos desde min_i hasta max_i con paso 's'
        i = min_i
        while i <= max_i + 1e-6:   # +epsilon para incluir el extremo
            if self.grid_plane == 0:  # plano XY (normal Z)
                # líneas paralelas a Z
                glVertex3f(i, self.grid_height, -grid_range)
                glVertex3f(i, self.grid_height,  grid_range)
                # líneas paralelas a X
                glVertex3f(-grid_range, self.grid_height, i)
                glVertex3f( grid_range, self.grid_height, i)

            elif self.grid_plane == 1:  # plano YZ (normal X)
                glVertex3f(self.grid_height, i, -grid_range)
                glVertex3f(self.grid_height, i,  grid_range)
                glVertex3f(self.grid_height, -grid_range, i)
                glVertex3f(self.grid_height,  grid_range, i)

            else:  # plano ZX (normal Y)
                glVertex3f(i, -grid_range, self.grid_height)
                glVertex3f(i,  grid_range, self.grid_height)
                glVertex3f(-grid_range, i, self.grid_height)
                glVertex3f( grid_range, i, self.grid_height)

            i += s
        glEnd()

    def render_object(self, obj):
        def transform_vertices(vertices, matrix):
            arr = np.array(vertices)  # (n, 3)
            n = arr.shape[0]
            ones = np.ones((n, 1))
            arr_hom = np.hstack([arr, ones])  # (n, 4)
            transformed = arr_hom @ matrix.T
            return [tuple(v[:3]) for v in transformed]

        vertices = obj.get_vertices()
        if hasattr(obj, "matrix"):
            vertices = transform_vertices(vertices, obj.matrix)

        glColor3f(1.0, 1.0, 1.0)
        if type(obj).__name__ == "Arc":
            glBegin(GL_LINE_STRIP)
            for vertex in vertices:
                glVertex3fv(vertex)
            glEnd()
        elif len(vertices) == 2:
            glBegin(GL_LINES)
            for vertex in vertices:
                glVertex3fv(vertex)
            glEnd()
        elif len(vertices) > 2:
            glBegin(GL_LINE_LOOP)
            for vertex in vertices:
                glVertex3fv(vertex)
            glEnd()
