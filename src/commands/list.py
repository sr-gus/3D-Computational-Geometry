from commands.base import Command

class ListCommand(Command):
    name = "list"
    min_args = 0
    max_args = 0
    usage = "Usage: list"

    def execute(self, args, renderer):
        if not renderer.objects:
            print("No hay objetos creados.")
            return
        for i, obj in enumerate(renderer.objects):
            print(f"{i}: {type(obj).__name__} - {obj}")