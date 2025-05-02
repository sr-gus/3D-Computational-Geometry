from geometry.primitives import Line
from commands.base import Command

class LineCommand(Command):
    name = "line"
    min_args = 6
    max_args = 6
    usage = "Usage: line x1 y1 z1 x2 y2 z2"

    def execute(self, args, renderer):
        try:
            coords = list(map(float, args))
        except ValueError:
            print("Error: Los parámetros deben ser numéricos.")
            return
        start = tuple(coords[:3])
        end = tuple(coords[3:])
        obj = Line(start, end)
        renderer.objects.append(obj)
        print(f"Linea agregada: {start} -> {end}")