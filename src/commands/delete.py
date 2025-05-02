from commands.base import Command

class DeleteCommand(Command):
    name = "delete"
    min_args = 1
    max_args = 1
    usage = "Usage: delete <índice>"

    def execute(self, args, renderer):
        try:
            idx = int(args[0])
            removed = renderer.objects.pop(idx)
            print(f"Objeto eliminado: {type(removed).__name__}")
        except (ValueError, IndexError):
            print("Índice inválido.")