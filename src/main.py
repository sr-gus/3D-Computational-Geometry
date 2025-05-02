import threading
import time
from input_handler import start_input_thread
from visualization.renderer import Renderer

def main():
    print("Bienvenido a 3D Computational Geometry")
    
    # Inicializar el renderizador
    renderer = Renderer()
    renderer.initialize_window()

    # Iniciar el hilo para procesar comandos desde la consola
    start_input_thread(renderer)

    # Bucle principal de renderizado
    while True:
        renderer.update_scene()
        time.sleep(0.01)

if __name__ == '__main__':
    main()
