from enum import Enum, auto


class ControlType(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()

    DROP = auto()

    ROTATE_LEFT = auto()
    ROTATE_RIGHT = auto()