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
    def __init__(self, center, radius):
        """
        center: Tupla (x, y, z)
        radius: Radio del círculo
        """
        self.center = center
        self.radius = radius

    def get_vertices(self):
        # Aquí podrías calcular los puntos que conforman el círculo
        return []