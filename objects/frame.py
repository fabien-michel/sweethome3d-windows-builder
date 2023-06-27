from obj_types.thickness import Thickness
import objects.vertex_normals as vn
from utils import get_id
from obj_types.part import Part


def new_frame(
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=2,
    thickness: Thickness = Thickness(5),
    mtl="white",
    id=None,
):
    return Part(
        name=get_id("frame"),
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
            ((1, 4, 3, 2), vn.FRONT),
            ((1, 9, 10, 4), vn.FRONT),
            ((2, 3, 14, 13), vn.FRONT),
            ((9, 13, 14, 10), vn.FRONT),
            ((5, 6, 7, 8), vn.BACK),
            ((5, 8, 12, 11), vn.BACK),
            ((6, 15, 16, 7), vn.BACK),
            ((11, 12, 16, 15), vn.BACK),
            ((4, 8, 7, 3), vn.TOP),
            ((4, 10, 12, 8), vn.RIGHT),
            ((3, 7, 16, 14), vn.LEFT),
            ((10, 14, 16, 12), vn.BOTTOM),
            ((1, 2, 6, 5), vn.BOTTOM),
            ((2, 13, 15, 6), vn.RIGHT),
            ((15, 13, 9, 11), vn.TOP),
            ((1, 5, 11, 9), vn.LEFT),
        ],
        smooth=False,
        mtl=mtl,
    )
