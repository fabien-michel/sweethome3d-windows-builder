from dataclasses import dataclass


@dataclass
class Thickness:
    top: float
    right: float
    bottom: float
    left: float

    def __init__(self, value):
        if isinstance(value, (int, float)):
            self.top = value
            self.right = value
            self.bottom = value
            self.left = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 2:
                self.top = value[0]
                self.bottom = value[0]
                self.right = value[1]
                self.left = value[1]
            if len(value) == 4:
                self.top = value[0]
                self.right = value[1]
                self.bottom = value[2]
                self.left = value[3]
        elif isinstance(value, Thickness):
            self.top = value.top
            self.right = value.right
            self.bottom = value.bottom
            self.left = value.left
