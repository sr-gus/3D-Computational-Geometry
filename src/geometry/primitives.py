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
    def __init__(self, center, radius, segments=32):
        """
        center: Tupla (x, y, z) que define el centro del círculo.
        radius: Radio del círculo.
        segments: Número de segmentos para aproximar el círculo.
        """
        self.center = center
        self.radius = radius
        self.segments = segments

    def get_vertices(self):
        vertices = []
        # Asumimos que el círculo se dibuja en el plano XY (Z fijo)
        for i in range(self.segments):
            theta = 2.0 * math.pi * i / self.segments
            x = self.center[0] + self.radius * math.cos(theta)
            y = self.center[1] + self.radius * math.sin(theta)
            z = self.center[2]
            vertices.append((x, y, z))
        return vertices