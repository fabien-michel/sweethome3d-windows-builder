from dataclasses import dataclass


@dataclass
class BaseObject:
    x: float = 0
    y: float = 0
    z: float = 0
    width: float = 1
    height: float = 1
    deep: float = 0.1
    name: float = "box"
    mtl: float = "white"
