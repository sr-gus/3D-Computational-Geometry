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
    else:
        print("Comando no reconocido.")
