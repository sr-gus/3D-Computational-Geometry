import math
from geometry.primitives import Arc
from commands.base import Command

class ArcGCommand(Command):
    name = "arcg"
    min_args = 10
    max_args = 11
    usage = "Usage: arcg start_x start_y start_z end_x end_y end_z offset_x offset_y direction [segments]"

    def execute(self, args, renderer):
        try:
            sx, sy, sz, ex, ey, ez = map(float, args[0:6])
            ox, oy = map(float, args[6:8])
            direction = args[8].lower()
            segments = int(args[9]) if len(args) == 10 else (int(args[9]) if len(args) == 11 else 32)
        except ValueError:
            print("Error: Parámetros numéricos inválidos.")
            return
        center = (sx + ox, sy + oy, sz)
        radius = math.hypot(ox, oy)
        sa = math.atan2(sy - center[1], sx - center[0])
        ea = math.atan2(ey - center[1], ex - center[0])
        cw_diff = (sa - ea) % (2 * math.pi)
        ccw_diff = (ea - sa) % (2 * math.pi)
        if abs(cw_diff - ccw_diff) < 1e-6:
            print("Aviso: arco de 180°; dirección no afecta.")
        if direction in ("cw", "horario", "h"):
            end_angle = sa - cw_diff
            dir_str = "Horario"
        elif direction in ("ccw", "antihorario", "ah"):
            end_angle = sa + ccw_diff
            dir_str = "Antihorario"
        else:
            print("Error: Dirección no reconocida.")
            return
        obj = Arc(center, radius, math.degrees(sa), math.degrees(end_angle), segments, "XY")
        renderer.objects.append(obj)
        print(f"ArcG agregado: centro={center}, radio={radius:.2f}, start={math.degrees(sa):.2f}°, end={math.degrees(end_angle):.2f}°, segmentos={segments}, dirección={dir_str}")