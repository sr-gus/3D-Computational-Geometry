# src/geometry/primitives.py
import math
import numpy as np

class Line:
    def __init__(self, start, end):
        """
        start, end: Tuplas (x, y, z)
        """
        self.start = start
        self.end = end
        self.matrix = np.identity(4)  # Matriz de transformación acumulada

    def get_vertices(self):
        return [self.start, self.end]

    def __str__(self):
        return f"Line from {self.start} to {self.end}"

class Circle:
    def __init__(self, center, radius, segments=32, plane="XY"):
        """
        center: Tupla (x, y, z) que define el centro del círculo.
        radius: Radio del círculo.
        segments: Número de segmentos para aproximar el círculo.
        plane: Plano ("XY", "XZ" o "YZ"); por defecto "XY".
        """
        self.center = center
        self.radius = radius
        self.segments = segments
        self.plane = plane.upper()
        self.matrix = np.identity(4)

    def get_vertices(self):
        vertices = []
        for i in range(self.segments):
            theta = 2.0 * math.pi * i / self.segments
            if self.plane == "XY":
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(theta)
                z = self.center[2]
            elif self.plane == "XZ":
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1]
                z = self.center[2] + self.radius * math.sin(theta)
            elif self.plane == "YZ":
                x = self.center[0]
                y = self.center[1] + self.radius * math.cos(theta)
                z = self.center[2] + self.radius * math.sin(theta)
            else:
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(theta)
                z = self.center[2]
            vertices.append((x, y, z))
        return vertices

    def __str__(self):
        return f"Circle with center {self.center} and radius {self.radius} in plane {self.plane}"

class Arc:
    def __init__(self, center, radius, start_angle, end_angle, segments=32, plane="XY"):
        """
        center: Tupla (x, y, z) que define el centro del arco.
        radius: Radio del arco.
        start_angle, end_angle: Ángulos en grados que definen el inicio y fin del arco.
        segments: Número de segmentos para aproximar el arco.
        plane: Plano ("XY", "XZ" o "YZ"); por defecto "XY".
        """
        self.center = center
        self.radius = radius
        # Convertir los ángulos a radianes.
        self.start_angle = math.radians(start_angle)
        self.end_angle = math.radians(end_angle)
        # Normalización sencilla: si end_angle es menor que start_angle y la diferencia es menor a 180° se suma 2π
        if self.end_angle < self.start_angle and (self.start_angle - self.end_angle) < math.pi:
            self.end_angle += 2 * math.pi
        self.segments = segments
        self.plane = plane.upper()
        self.matrix = np.identity(4)

    def get_vertices(self):
        vertices = []
        angle_range = self.end_angle - self.start_angle
        for i in range(self.segments + 1):
            theta = self.start_angle + angle_range * i / self.segments
            if self.plane == "XY":
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(theta)
                z = self.center[2]
            elif self.plane == "XZ":
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1]
                z = self.center[2] + self.radius * math.sin(theta)
            elif self.plane == "YZ":
                x = self.center[0] + 0,  # opcionalmente podrías ajustar aquí, pero se asume movimiento en YZ
                y = self.center[1] + self.radius * math.cos(theta)
                z = self.center[2] + self.radius * math.sin(theta)
                # Para mantener la coherencia, usaremos la rama else igual que XY
                # (si se requiere ajustar, modificar esta sección)
            elif self.plane == "YZ":
                x = self.center[0]
                y = self.center[1] + self.radius * math.cos(theta)
                z = self.center[2] + self.radius * math.sin(theta)
            else:
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(theta)
                z = self.center[2]
            vertices.append((x, y, z))
        return vertices

    def __str__(self):
        return (f"Arc with center {self.center}, radius {self.radius}, "
                f"start_angle {math.degrees(self.start_angle):.1f}°, "
                f"end_angle {math.degrees(self.end_angle):.1f}° in plane {self.plane}")