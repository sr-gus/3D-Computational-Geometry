from commands.base import Command

class HelpCommand(Command):
    name = "help"
    min_args = 0
    max_args = 0
    usage = "Usage: help"

    def execute(self, args, renderer):
        from commands import all_commands
        print("Available commands:")
        for cmd in all_commands:
            print(f"  {cmd.name}: {cmd.usage}")