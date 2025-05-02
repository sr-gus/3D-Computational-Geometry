from abc import ABC, abstractmethod
from typing import List, Optional

class Command(ABC):
    """
    Base class for all commands. Subclasses should define:
      - name: command keyword (str)
      - min_args: minimum number of args
      - max_args: maximum number of args (None for no limit)
      - usage: usage string to display on invalid input
    """
    name: str = ""
    min_args: int = 0
    max_args: Optional[int] = None
    usage: str = ""

    def run(self, args: List[str], renderer):
        # Validate argument count
        if len(args) < self.min_args or (self.max_args is not None and len(args) > self.max_args):
            print(self.usage)
            return
        try:
            self.execute(args, renderer)
        except Exception as e:
            print(f"Error: {e}")

    @abstractmethod
    def execute(self, args: List[str], renderer):
        pass