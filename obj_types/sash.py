from dataclasses import dataclass


@dataclass
class Sash:
    x_axis: float = 0
    y_axis: float = 0
    width: float = 0
    start_angle: float = 0
    end_angle: float = 0
