from utils import get_id
from obj_types.part import Part
import objects.vertex_normals as vn


def new_box(x=0, y=0, z=0, width=1, height=1, depth=0.1, name="box", mtl="white"):
    return Part(
        name=get_id(name),
        vertices=[
            (x, y, z),
            (x + width, y, z),
            (x + width, y + height, z),
            (x, y + height, z),
            (x, y, z + depth),
            (x + width, y, z + depth),
            (x + width, y + height, z + depth),
            (x, y + height, z + depth),
        ],
        faces=[
            ((1, 2, 3, 4), vn.FRONT),
            ((5, 6, 7, 8), vn.BACK),
            ((1, 2, 6, 5), vn.BOTTOM),
            ((1, 5, 8, 4), vn.LEFT),
            ((2, 3, 7, 6), vn.RIGHT),
            ((3, 4, 8, 7), vn.TOP),
        ],
        smooth=False,
        mtl=mtl,
    )
