from geometry.primitives import Arc
from commands.base import Command

class ArcCommand(Command):
    name = "arc"
    min_args = 7
    max_args = 9
    usage = "Usage: arc x y z radius start_angle end_angle [segments] [plane]"

    def execute(self, args, renderer):
        try:
            x, y, z = map(float, args[0:3])
            radius = float(args[3])
            start_angle = float(args[4])
            end_angle = float(args[5])
        except ValueError:
            print("Error: Los parámetros x, y, z, radius, start_angle y end_angle deben ser numéricos.")
            return
        segments = 32
        plane = "XY"
        if len(args) >= 7:
            opt = args[6]
            try:
                segments = int(opt)
                if len(args) >= 8:
                    plane = args[7].upper()
            except ValueError:
                plane = opt.upper()
        if plane not in ("XY", "XZ", "YZ"):
            print("Error: Plano inválido. Usa XY, XZ o YZ.")
            return
        obj = Arc((x, y, z), radius, start_angle, end_angle, segments, plane)
        renderer.objects.append(obj)
        print(f"Arco agregado: centro=({x}, {y}, {z}), radio={radius}, start={start_angle}°, end={end_angle}°, segmentos={segments}, plano={plane}")