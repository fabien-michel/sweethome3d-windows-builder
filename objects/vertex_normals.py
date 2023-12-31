from enum import Enum


class VN(Enum):
    RIGHT = (1.0, 0.0, 0.0)
    LEFT = (-1.0, 0.0, 0.0)
    TOP = (0.0, 1.0, 0.0)
    BOTTOM = (0.0, -1.0, 0.0)
    BACK = (0.0, 0.0, -1.0)
    FRONT = (0.0, 0.0, 1.0)
