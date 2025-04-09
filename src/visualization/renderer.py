import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Renderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.objects = []  # Lista de objetos geométricos
        self.mouse_down = False
        self.last_mouse_pos = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = 5.0  # Distancia inicial de la cámara
        # Control de la cuadrícula
        self.show_grid = False
        self.grid_height = 0.0  # Altura a la que se dibuja la cuadrícula

    def initialize_window(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)

        # Configurar la matriz de proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width / self.height), 0.1, 50.0)

        # Volver al modo de modelo y posicionar la cámara
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.zoom)

        glLineWidth(2.0)
        print("Ventana inicializada")

    def update_scene(self):
        # Procesar eventos: mouse y teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo: iniciar rotación
                    self.mouse_down = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up: zoom in
                    self.zoom = max(1.0, self.zoom - 0.5)
                elif event.button == 5:  # Scroll down: zoom out
                    self.zoom += 0.5
                print("Zoom: " + str(self.zoom))

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
                # Alternar visibilidad de la cuadrícula con "g"
                if event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                    print("Grid toggled:", self.show_grid)
                # Ajustar la altura de la cuadrícula con las flechas arriba/abajo
                elif event.key == pygame.K_UP:
                    self.grid_height += 0.5
                    print("Grid height:", self.grid_height)
                elif event.key == pygame.K_DOWN:
                    self.grid_height -= 0.5
                    print("Grid height:", self.grid_height)

        # Configurar la escena
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.zoom)  # Aplicar el zoom
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # Dibujar ejes (opcional: puedes dejarlo si lo deseas o quitarlo)
        self.draw_axes()

        # Dibujar la cuadrícula si está activada
        if self.show_grid:
            self.draw_grid()

        # Renderizar cada objeto en la lista (por ejemplo, líneas dibujadas por el usuario)
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
        # Dibujar la cuadrícula en el plano XZ a una altura determinada (self.grid_height)
        glColor3f(0.5, 0.5, 0.5)  # Gris
        glBegin(GL_LINES)
        grid_range = max(2.0, 2 * self.zoom)  # Extensión de la cuadrícula en cada dirección
        step = 1.0
        # Líneas paralelas al eje Z (con X variable)
        for i in np.arange(-grid_range, grid_range + step, step):
            glVertex3f(i, self.grid_height, -grid_range)
            glVertex3f(i, self.grid_height, grid_range)
        # Líneas paralelas al eje X (con Z variable)
        for i in np.arange(-grid_range, grid_range + step, step):
            glVertex3f(-grid_range, self.grid_height, i)
            glVertex3f(grid_range, self.grid_height, i)
        glEnd()

    def render_object(self, obj):
        vertices = obj.get_vertices()
        # Suponemos que para líneas se poseen 2 vértices
        if len(vertices) == 2:
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINES)
            for vertex in vertices:
                glVertex3fv(vertex)
            glEnd()
        elif len(vertices) > 2:
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINE_LOOP)
            for vertex in vertices:
                glVertex3fv(vertex)
            glEnd()