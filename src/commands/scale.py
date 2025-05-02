from transforms.transformations import apply_scale
from commands.base import Command

class ScaleCommand(Command):
    name = "escalate"
    min_args = 2
    max_args = 2
    usage = "Usage: escalate <id|all> factor"

    def execute(self, args, renderer):
        target = args[0].lower()
        try:
            factor = float(args[1])
        except ValueError:
            print("Error: El factor de escala debe ser numérico.")
            return
        objs = renderer.objects if target == 'all' else [renderer.objects[int(target)]]
        for obj in objs:
            apply_scale(obj, factor)
        print(f"Escalado aplicado a {target}: {factor}")