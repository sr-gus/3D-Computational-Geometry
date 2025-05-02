from geometry.primitives import Circle
from commands.base import Command

class CircleCommand(Command):
    name = "circle"
    min_args = 5
    max_args = 7
    usage = "Usage: circle x y z radius [segments] [plane]"

    def execute(self, args, renderer):
        # Parse required parameters
        try:
            x, y, z, radius = map(float, args[:4])
        except ValueError:
            print("Error: Los parámetros x, y, z y radius deben ser numéricos.")
            return
        segments = 32
        plane = "XY"
        # Optional fifth argument: segments or plane
        if len(args) >= 5:
            opt = args[4]
            try:
                segments = int(opt)
                if len(args) >= 6:
                    plane = args[5].upper()
            except ValueError:
                plane = opt.upper()
        # Validate plane
        if plane not in ("XY", "XZ", "YZ"):
            print("Error: Plano inválido. Usa XY, XZ o YZ.")
            return
        obj = Circle((x, y, z), radius, segments, plane)
        renderer.objects.append(obj)
        print(f"Círculo agregado: centro=({x}, {y}, {z}), radio={radius}, segmentos={segments}, plano={plane}")