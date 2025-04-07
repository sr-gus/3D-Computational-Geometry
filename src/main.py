import threading
import time
from input_handler import process_command
from visualization.renderer import Renderer

def command_input_loop(renderer):
    while True:
        command = input("Ingresa un comando (o 'salir' para terminar): ")
        if command.lower() in ['salir', 'exit']:
            print("Terminando...")
            import os
            os._exit(0)
        process_command(command, renderer)

def main():
    print("Bienvenido a 3D Computational Geometry")
    
    # Inicializar el renderizador
    renderer = Renderer()
    renderer.initialize_window()

    # Iniciar el hilo para procesar comandos desde la consola
    thread = threading.Thread(target=command_input_loop, args=(renderer,), daemon=True)
    thread.start()

    # Bucle principal de renderizado
    while True:
        renderer.update_scene()
        time.sleep(0.01)

if __name__ == '__main__':
    main()
