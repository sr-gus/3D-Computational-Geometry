from transforms.transformations import apply_reflection
from commands.base import Command

class ReflectCommand(Command):
    name = "reflect"
    min_args = 2
    max_args = 2
    usage = "Usage: reflect <id|all> <plane>"

    def execute(self, args, renderer):
        target = args[0].lower()
        plane = args[1].upper()
        if plane not in ("XY", "XZ", "YZ"):
            print("Error: Plano desconocido. Usa 'XY', 'XZ' o 'YZ'.")
            return
        objs = renderer.objects if target == 'all' else [renderer.objects[int(target)]]
        for obj in objs:
            apply_reflection(obj, plane)
        print(f"Reflexión aplicada a {target} respecto al plano {plane}")