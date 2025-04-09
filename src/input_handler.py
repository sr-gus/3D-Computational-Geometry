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
        # Se espera: circle x y z radius [segments]
        if len(tokens) < 5:
            print("Uso: circle x y z radius [segments]")
            return
        try:
            x, y, z = float(tokens[1]), float(tokens[2]), float(tokens[3])
            radius = float(tokens[4])
            segments = int(tokens[5]) if len(tokens) >= 6 else 32
            from geometry.primitives import Circle
            new_circle = Circle((x, y, z), radius, segments)
            renderer.objects.append(new_circle)
            print(f"Círculo agregado: centro=({x}, {y}, {z}), radio={radius}, segmentos={segments}")
        except ValueError:
            print("Error: Los parámetros deben ser numéricos.")
    else:
        print("Comando no reconocido.")
