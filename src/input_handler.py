import threading
from commands import all_commands

def input_loop(renderer):
    while True:
        raw = input('> ')
        if not raw:
            continue
        parts = raw.strip().split()
        cmd_name, args = parts[0].lower(), parts[1:]
        for cmd in all_commands:
            if cmd.name == cmd_name:
                cmd.run(args, renderer)
                break
        else:
            print(f"Comando no reconocido: {cmd_name}")

def start_input_thread(renderer):
    t = threading.Thread(target=input_loop, args=(renderer,), daemon=True)
    t.start()