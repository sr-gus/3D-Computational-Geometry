# src/transforms/transformations.py
import numpy as np
import math

def rotation_matrix_x(theta):
    """
    Retorna la matriz 4x4 de rotación para 'theta' grados alrededor del eje X.
    """
    rad = math.radians(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(rad), -math.sin(rad), 0],
        [0, math.sin(rad), math.cos(rad), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(theta):
    """
    Retorna la matriz 4x4 de rotación para 'theta' grados alrededor del eje Y.
    """
    rad = math.radians(theta)
    return np.array([
        [math.cos(rad), 0, math.sin(rad), 0],
        [0, 1, 0, 0],
        [-math.sin(rad), 0, math.cos(rad), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(theta):
    """
    Retorna la matriz 4x4 de rotación para 'theta' grados alrededor del eje Z.
    """
    rad = math.radians(theta)
    return np.array([
        [math.cos(rad), -math.sin(rad), 0, 0],
        [math.sin(rad), math.cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def translation_matrix(dx, dy, dz):
    """
    Retorna una matriz 4x4 de traslación.
    """
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def apply_translation(target, dx, dy, dz):
    """
    Aplica una transformación de traslación al objeto.
    """
    if hasattr(target, "matrix"):
        T = translation_matrix(dx, dy, dz)
        target.matrix = T @ target.matrix

def rotate(target, *angles, axis=None):
    """
    Función única de entrada para aplicar rotaciones.

    Parámetros:
      - target: Puede ser:
          a) un punto 3D (tupla de 3 números), en cuyo caso se devuelve el punto rotado, o
          b) un objeto que tenga el atributo 'matrix' (como nuestras primitivas), en cuyo
             caso se actualiza su matriz de transformación global (multiplicación a la izquierda).
      - angles:
          • Si se proporciona el parámetro 'axis' (string "x", "y", "z"), se espera que se pase un único ángulo.
          • Si 'axis' es None, se esperan tres ángulos (angle_x, angle_y, angle_z) que se combinarán
            en el orden global: R = Rz * Ry * Rx.
      - axis: (opcional) Una cadena: "x", "y" o "z". Si se especifica, se usa la rotación en ese eje.

    Retorna:
      - Si el target es un punto: la nueva posición del punto (tupla de 3 elementos).
      - Si el target es un objeto con atributo 'matrix': lo actualiza (no retorna nada en particular).
      - Si target es None, retorna la matriz de rotación resultante.
    """
    # Construir la matriz de rotación R
    R = None
    if axis is not None:
        if len(angles) != 1:
            raise ValueError("For single axis rotation, provide exactly one angle.")
        a = float(angles[0])
        axis = axis.lower()
        if axis == "x":
            R = rotation_matrix_x(a)
        elif axis == "y":
            R = rotation_matrix_y(a)
        elif axis == "z":
            R = rotation_matrix_z(a)
        else:
            raise ValueError("Unknown axis. Use 'x', 'y', or 'z'.")
    else:
        if len(angles) != 3:
            raise ValueError("For three-axis rotation, provide three angles (angle_x, angle_y, angle_z).")
        angle_x, angle_y, angle_z = map(float, angles)
        R_x = rotation_matrix_x(angle_x)
        R_y = rotation_matrix_y(angle_y)
        R_z = rotation_matrix_z(angle_z)
        # Orden global: primero aplicar rotación en X, luego Y y finalmente Z
        R = R_z @ R_y @ R_x

    # Si no se especifica target, se devuelve la matriz
    if target is None:
        return R
    # Si target es un punto (tupla de 3 elementos)
    if isinstance(target, tuple) and len(target) == 3:
        p_hom = np.array(list(target) + [1])
        p_rot = p_hom @ R.T
        return tuple(p_rot[:3])
    # Si target es un objeto con atributo 'matrix'
    if hasattr(target, "matrix"):
        target.matrix = R @ target.matrix
        return target

    # Caso por defecto: retorna la matriz (aunque no se debería llegar aquí)
    return R

def scaling_matrix(factor):
    """
    Retorna una matriz 4x4 de escalado uniforme.
    """
    return np.array([
        [factor, 0, 0, 0],
        [0, factor, 0, 0],
        [0, 0, factor, 0],
        [0, 0, 0, 1]
    ])

def apply_scale(target, factor):
    """
    Aplica una transformación de escalado al objeto.
    """
    if hasattr(target, "matrix"):
        S = scaling_matrix(factor)
        target.matrix = S @ target.matrix

def reflection_matrix(plane):
    """
    Retorna la matriz 4×4 que refleja respecto al plano indicado:
      - "XY": invierte Z
      - "XZ": invierte Y
      - "YZ": invierte X
    """
    p = plane.upper()
    if p == "XY":
        # Z → −Z
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ])
    elif p == "XZ":
        # Y → −Y
        return np.array([
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    elif p == "YZ":
        # X → −X
        return np.array([
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    else:
        raise ValueError("reflection_matrix: Unknown plane. Use 'XY', 'XZ' or 'YZ'.")

def apply_reflection(target, plane):
    """
    Aplica simetría (reflexión) al objeto o punto:
      - Si target es un objeto con `matrix`, le multiplica la matriz de reflexión a la izquierda.
      - Si target es un punto (x,y,z), devuelve el punto reflejado.
    """
    R = reflection_matrix(plane)
    # punto
    if isinstance(target, tuple) and len(target) == 3:
        p_hom = np.array(list(target) + [1])
        p_ref = p_hom @ R.T
        return tuple(p_ref[:3])
    # objeto con matriz
    if hasattr(target, "matrix"):
        target.matrix = R @ target.matrix
        return target
    # si no es ninguno, devolvemos la matriz pura
    return R