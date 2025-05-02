from typing import List
from .base import Command
from .help import HelpCommand
from .line import LineCommand
from .circle import CircleCommand
from .arc import ArcCommand
from .arcg import ArcGCommand
from .list import ListCommand
from .delete import DeleteCommand
from .rotate import RotateCommand
from .translate import TranslateCommand
from .scale import ScaleCommand
from .reflect import ReflectCommand
from .grid import MoveGridCommand, GridStepCommand

all_commands: List[Command] = [
    HelpCommand(), LineCommand(), CircleCommand(), ArcCommand(), ArcGCommand(),
    ListCommand(), DeleteCommand(),
    RotateCommand(), TranslateCommand(), ScaleCommand(), ReflectCommand(),
    MoveGridCommand(), GridStepCommand(),
]