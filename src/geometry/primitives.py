import math

class Line:
    def __init__(self, start, end):
        """
        start, end: Tuplas (x, y, z)
        """
        self.start = start
        self.end = end

    def get_vertices(self):
        return [self.start, self.end]

class Circle:
    def __init__(self, center, radius, segments=32, plane="XY"):
        """
        center: Tupla (x, y, z) que define el centro del círculo.
        radius: Radio del círculo.
        segments: Número de segmentos para aproximar el círculo.
        plane: String que indica en qué plano se dibujará el círculo.
               Puede ser "XY", "XZ" o "YZ". Por defecto se usa "XY".
        """
        self.center = center
        self.radius = radius
        self.segments = segments
        self.plane = plane.upper()  # Se asegura de que esté en mayúsculas

    def get_vertices(self):
        vertices = []
        for i in range(self.segments):
            theta = 2.0 * math.pi * i / self.segments
            # Generar vértices según el plano especificado:
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
                # Si se proporciona un valor no reconocido, se asume el plano XY
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(theta)
                z = self.center[2]
            vertices.append((x, y, z))
        return vertices

class Arc:
    def __init__(self, center, radius, start_angle, end_angle, segments=32, plane="XY"):
        """
        center: Tupla (x, y, z) que define el centro del arco.
        radius: Radio del arco.
        start_angle, end_angle: Ángulos en grados que definen el inicio y fin del arco.
        segments: Número de segmentos para aproximar el arco (por defecto 32).
        plane: Plano en el que se dibuja el arco ("XY", "XZ" o "YZ"). Por defecto "XY".
        """
        self.center = center
        self.radius = radius
        # Convertir los ángulos de grados a radianes.
        self.start_angle = math.radians(start_angle)
        self.end_angle = math.radians(end_angle)
        # Si end_angle queda menor que start_angle, se asume un giro completo (se le suma 2π)
        if self.end_angle < self.start_angle:
            self.end_angle += 2 * math.pi
        self.segments = segments
        self.plane = plane.upper()

    def get_vertices(self):
        vertices = []
        angle_range = self.end_angle - self.start_angle
        # Usamos segments+1 para incluir el punto final
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
                x = self.center[0]
                y = self.center[1] + self.radius * math.cos(theta)
                z = self.center[2] + self.radius * math.sin(theta)
            else:
                x = self.center[0] + self.radius * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(theta)
                z = self.center[2]
            vertices.append((x, y, z))
        return vertices