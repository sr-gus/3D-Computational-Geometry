import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

    def draw_axes(self):
        glLineWidth(2.0)
        glBegin(GL_LINES)
        # Eje X: Rojo
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(2.0, 0.0, 0.0)
        
        # Eje Y: Verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 2.0, 0.0)
        
        # Eje Z: Azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 2.0)
        glEnd()

    def update_scene(self):
        # Procesar eventos de Pygame (incluyendo eventos del mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo: iniciar rotación
                    self.mouse_down = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up: zoom in (acercar)
                    self.zoom = max(1.0, self.zoom - 0.5)
                elif event.button == 5:  # Scroll down: zoom out (alejar)
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

        # Configurar la escena
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -self.zoom)  # Aplicar el zoom
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # Dibujar los ejes
        self.draw_axes()

        # Renderizar cada objeto en la lista
        for obj in self.objects:
            self.render_object(obj)
        
        pygame.display.flip()
        pygame.time.wait(10)

    def render_object(self, obj):
        vertices = obj.get_vertices()
        if len(vertices) == 2:
            glColor3f(1.0, 1.0, 1.0)  # Dibujar la línea en blanco
            glBegin(GL_LINES)
            for vertex in vertices:
                glVertex3fv(vertex)
            glEnd()
