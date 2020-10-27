from enum import Enum, unique, auto


@unique
class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    CYAN = auto()
    MAGENTA = auto()
    YELLOW = auto()
    WHITE = auto()
    BLACK = auto()