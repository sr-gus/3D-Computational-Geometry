import math

def process_command(command, renderer):
    tokens = command.split()
    if not tokens:
        return

    cmd = tokens[0].lower()
    if cmd == "line":
        if len(tokens) == 7:
            try:
                coords = list(map(float, tokens[1:]))
                start = tuple(coords[:3])
                end = tuple(coords[3:])
                from geometry.primitives import Line
                new_line = Line(start, end)
                renderer.objects.append(new_line)
                print(f"Linea agregada: {start} -> {end}")
            except ValueError:
                print("Error: Los parámetros deben ser numéricos.")
        else:
            print("Uso: line x1 y1 z1 x2 y2 z2")

    elif cmd == "circle":
        # Se espera: circle x y z radius [segments] [plane]
        if len(tokens) < 5:
            print("Uso: circle x y z radius [segments] [plane]")
            return
        try:
            x, y, z = float(tokens[1]), float(tokens[2]), float(tokens[3])
            radius = float(tokens[4])
        except ValueError:
            print("Error: Los parámetros x, y, z y radius deben ser numéricos.")
            return

        # Valores por defecto para segmentos y plano
        segments = 32
        plane = "XY"

        # Si hay un sexto parámetro, se intenta convertirlo a entero (segmentos)
        if len(tokens) >= 6:
            try:
                segments = int(tokens[5])
                # Si hay un séptimo parámetro, se toma como el plano
                if len(tokens) >= 7:
                    plane = tokens[6]
            except ValueError:
                # Si la conversión falla, se asume que el sexto parámetro es el plano
                plane = tokens[5]

        from geometry.primitives import Circle
        new_circle = Circle((x, y, z), radius, segments, plane)
        renderer.objects.append(new_circle)
        print(f"Círculo agregado: centro=({x}, {y}, {z}), radio={radius}, segmentos={segments}, plano={plane.upper()}")

    elif cmd == "arc":
        # Se espera: arc x y z radius start_angle end_angle [segments] [plane]
        if len(tokens) < 7:
            print("Uso: arc x y z radius start_angle end_angle [segments] [plane]")
            return
        try:
            x, y, z = float(tokens[1]), float(tokens[2]), float(tokens[3])
            radius = float(tokens[4])
            start_angle = float(tokens[5])
            end_angle = float(tokens[6])
        except ValueError:
            print("Error: Los parámetros x, y, z, radius, start_angle y end_angle deben ser numéricos.")
            return

        segments = 32
        plane = "XY"
        if len(tokens) >= 8:
            try:
                segments = int(tokens[7])
                if len(tokens) >= 9:
                    plane = tokens[8]
            except ValueError:
                # Si no se puede convertir a int, se asume que es el plano
                plane = tokens[7]
        from geometry.primitives import Arc
        new_arc = Arc((x, y, z), radius, start_angle, end_angle, segments, plane)
        renderer.objects.append(new_arc)
        print("Arco agregado: centro=({}, {}, {}), radio={}, start_angle={}°, end_angle={}°, segmentos={}, plano={}".format(
            x, y, z, radius, start_angle, end_angle, segments, plane.upper()
        ))

    elif cmd == "arcg":
        # Sintaxis: arcG start_x start_y start_z end_x end_y end_z offset_x offset_y direction [segments]
        if len(tokens) < 10:
            print("Uso: arcG start_x start_y start_z end_x end_y end_z offset_x offset_y direction [segments]")
            return
        try:
            start_x = float(tokens[1])
            start_y = float(tokens[2])
            start_z = float(tokens[3])
            end_x   = float(tokens[4])
            end_y   = float(tokens[5])
            end_z   = float(tokens[6])
            offset_x = float(tokens[7])
            offset_y = float(tokens[8])
            direction = tokens[9].lower()  # Se espera 'cw' o 'ccw'
            segments = 32
            if len(tokens) >= 11:
                segments = int(tokens[10])
        except ValueError:
            print("Error: Alguno de los parámetros numéricos es inválido (excepto la dirección).")
            return

        # Calcular el centro (se asume trabajo en el plano XY)
        center = (start_x + offset_x, start_y + offset_y, start_z)
        # Radio: distancia entre el centro y el punto de inicio (solo en XY)
        radius = math.sqrt(offset_x**2 + offset_y**2)
        # Calcular ángulos en radianes (con respecto al centro) para inicio y fin
        start_angle = math.atan2(start_y - center[1], start_x - center[0])
        end_angle   = math.atan2(end_y   - center[1], end_x   - center[0])
        
        # Calcular las diferencias de ángulo:
        cw_diff  = (start_angle - end_angle) % (2*math.pi)
        ccw_diff = (end_angle - start_angle) % (2*math.pi)
        
        # Si la diferencia entre cw_diff y ccw_diff es casi nula, se trata de un arco de 180°
        if abs(cw_diff - ccw_diff) < 1e-6:
            print("Aviso: El arco es de 180°; en estos casos, la dirección (CW/CCW) no afecta el resultado.")

        # Según el parámetro de dirección, se ajusta el ángulo final
        if direction in ["cw", "horario", "h"]:
            # Para el sentido horario, queremos que el recorrido sea de 'cw_diff'
            end_angle_actual = start_angle - cw_diff
        elif direction in ["ccw", "antihorario", "ah"]:
            # Para el sentido antihorario, usamos 'ccw_diff'
            end_angle_actual = start_angle + ccw_diff
        else:
            print("Error: Dirección no reconocida. Usa 'CW' para horario o 'CCW' para antihorario.")
            return

        from geometry.primitives import Arc
        new_arc = Arc(center, radius,
                      math.degrees(start_angle),
                      math.degrees(end_angle_actual),
                      segments, "XY")
        renderer.objects.append(new_arc)
        print(f"ArcG agregado: centro={center}, radio={radius:.2f}, "
              f"start_angle={math.degrees(start_angle):.2f}°, "
              f"end_angle={math.degrees(end_angle_actual):.2f}°, "
              f"segmentos={segments}, dirección={'Horario' if direction in ['cw','horario','h'] else 'Antihorario'}")
            
    else:
        print("Comando no reconocido.")