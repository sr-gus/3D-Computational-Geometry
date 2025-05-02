import time
from visualization.renderer import Renderer
from input_handler import start_input_thread


def main():
    print("Bienvenido a 3D Computational Geometry")
    print("Escribe 'help' para ver la lista de comandos disponibles.")
    print("Dentro de la ventana: presiona 'g' para alternar el grid, usa las flechas para mover el grid o cambiar su plano, y desplaza la rueda del mouse para hacer zoom.")

    # Inicializar el renderizador y ventana
    renderer = Renderer()
    renderer.initialize_window()

    # Iniciar hilo de comandos desde la consola
    start_input_thread(renderer)

    # Bucle principal de renderizado
    try:
        while True:
            renderer.update_scene()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Saliendo...")


if __name__ == '__main__':
    main()