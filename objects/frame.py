from obj_types.thickness import Thickness
from obj_types.part import Part


def new_frame(
    name="frame",
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=2,
    thickness: Thickness = Thickness(5),
    mtl="white",
):
    return Part(
        name=name,
        vertices=[
            (x, y, z),  # 1
            (x + width, y, z),  # 2
            (x + width - thickness.right, y + thickness.bottom, z),  # 3
            (x + thickness.left, y + thickness.bottom, z),  # 4
            #
            (x, y, z + depth),  # 5
            (x + width, y, z + depth),  # 6
            (x + width - thickness.right, y + thickness.bottom, z + depth),  # 7
            (x + thickness.left, y + thickness.bottom, z + depth),  # 8
            #
            (x, y + height, z),  # 9
            (x + thickness.left, y + height - thickness.top, z),  # 10
            #
            (x, y + height, z + depth),  # 11
            (x + thickness.left, y + height - thickness.top, z + depth),  # 12
            #
            (x + width, y + height, z),  # 13
            (x + width - thickness.right, y + height - thickness.top, z),  # 14
            (x + width, y + height, z + depth),  # 15
            (x + width - thickness.right, y + height - thickness.top, z + depth),  # 16
        ],
        faces=[
            (1, 4, 3, 2),
            (1, 9, 10, 4),
            (2, 3, 14, 13),
            (9, 13, 14, 10),
            (5, 6, 7, 8),
            (5, 8, 12, 11),
            (6, 15, 16, 7),
            (11, 12, 16, 15),
            (4, 8, 7, 3),
            (4, 10, 12, 8),
            (3, 7, 16, 14),
            (10, 14, 16, 12),
            (1, 2, 6, 5),
            (2, 13, 15, 6),
            (15, 13, 9, 11),
            (1, 5, 11, 9),
        ],
        smooth=False,
        mtl=mtl,
    )
