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

class Arc:
    def __init__(self, center, radius, start_angle, end_angle):
        """
        center: Tupla (x, y, z)
        radius: Radio del arco
        start_angle, end_angle: Ángulos en radianes
        """
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def get_vertices(self):
        # Aquí podrías calcular los puntos a lo largo del arco
        return []

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