import numpy as np

def translate(point, vector):
    """
    Traslada un punto aplicando el vector de traslación.
    point, vector: Tuplas o arrays de 3 elementos.
    """
    return tuple(np.array(point) + np.array(vector))

def rotate(point, axis, angle):
    """
    Rota un punto alrededor de un eje dado.
    axis: Tupla (x, y, z) que define el eje.
    angle: Ángulo en radianes.
    NOTA: Implementa la matriz de rotación correspondiente.
    """
    # Aquí se debería construir y aplicar la matriz de rotación
    return point  # Placeholder

def scale(point, factor):
    """
    Escala un punto por el factor dado.
    """
    return tuple(np.array(point) * factor)