from commands.base import Command

class MoveGridCommand(Command):
    name = "move_grid"
    min_args = 1
    max_args = 1
    usage = "Usage: move_grid <position>"

    def execute(self, args, renderer):
        try:
            pos = float(args[0])
        except ValueError:
            print("Error: El position debe ser numérico.")
            return
        renderer.grid_height = pos
        print(f"Grid movida a {pos}.")

class GridStepCommand(Command):
    name = "grid_step"
    min_args = 1
    max_args = 1
    usage = "Usage: grid_step <step>"

    def execute(self, args, renderer):
        try:
            step = float(args[0])
        except ValueError:
            print("Error: El step debe ser numérico.")
            return
        if step == 0:
            print("El step debe ser diferente de cero.")
            return
        renderer.grid_step = step
        print(f"Step del grid cambiado a {step}.")