from transforms.transformations import rotate as transform_rotate
from commands.base import Command

class RotateCommand(Command):
    name = "rotate"
    min_args = 3
    max_args = 4
    usage = "Usage: rotate <id|all> <axis> <angle> OR rotate <id|all> <angle_x> <angle_y> <angle_z>"

    def execute(self, args, renderer):
        target = args[0].lower()
        # Syntax 1: single-axis
        if len(args) == 3:
            axis = args[1].lower()
            try:
                angle = float(args[2])
            except ValueError:
                print("Error: Angle must be numeric.")
                return
            objs = renderer.objects if target == 'all' else [renderer.objects[int(target)]]
            for obj in objs:
                transform_rotate(obj, angle, axis=axis)
            print(f"Rotation applied to {target} on axis {axis} by {angle}°")
        # Syntax 2: triple-angle
        elif len(args) == 4:
            try:
                ax, ay, az = map(float, args[1:4])
            except ValueError:
                print("Error: Angles must be numeric.")
                return
            objs = renderer.objects if target == 'all' else [renderer.objects[int(target)]]
            for obj in objs:
                transform_rotate(obj, ax, ay, az)
            print(f"Rotation applied to {target} with angles ({ax}, {ay}, {az})°")
        else:
            print(self.usage)