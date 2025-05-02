from transforms.transformations import apply_translation
from commands.base import Command

class TranslateCommand(Command):
    name = "translate"
    min_args = 4
    max_args = 4
    usage = "Usage: translate <id|all> dx dy dz"

    def execute(self, args, renderer):
        target = args[0].lower()
        try:
            dx, dy, dz = map(float, args[1:4])
        except ValueError:
            print("Error: Los desplazamientos deben ser numéricos.")
            return
        objs = renderer.objects if target == 'all' else [renderer.objects[int(target)]]
        for obj in objs:
            apply_translation(obj, dx, dy, dz)
        print(f"Traslación aplicada a {target}: ({dx}, {dy}, {dz})")