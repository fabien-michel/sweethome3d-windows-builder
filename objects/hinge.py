from utils import get_id
from obj_types.part import Part
import objects.vertex_normals as vn


def new_hinge(id, x=0, y=0, z=0):
    x += 0.6
    z += 1.0
    y -= 2.0
    return Part(
        name=get_id(f"sweethome3d_hinge_{id}"),
        vertices=[
            (x, y, z),
            (x + 0.293, y, z + 0.707),
            (x + -0.707, y, z + 0.707),
            (x + -0.707, y, z + -0.293),
            (x + -1.414, y, z),
            (x + -1.707, y, z + 0.707),
            (x + -1.414, y, z + 1.414),
            (x + -0.707, y, z + 1.707),
            (x, y, z + 1.414),
            (x + -1.414, y + 4.0, z + 1.414),
            (x + -0.707, y + 4.0, z + 1.707),
            (x + -1.414, y + 4.0, z),
            (x + -1.707, y + 4.0, z + 0.707),
            (x + 0.293, y + 4.0, z + 0.707),
            (x, y + 4.0, z),
            (x + -0.707, y + 4.0, z + -0.293),
            (x, y + 4.0, z + 1.414),
            (x + -0.707, y + 4.0, z + 0.707),
        ],
        faces=[
            ((1, 2, 3), vn.FRONT),
            ((4, 1, 3), vn.FRONT),
            ((5, 4, 3), vn.FRONT),
            ((6, 5, 3), vn.FRONT),
            ((7, 6, 3), vn.FRONT),
            ((8, 7, 3), vn.FRONT),
            ((9, 8, 3), vn.FRONT),
            ((2, 9, 3), vn.FRONT),
            ((10, 7, 8, 11), vn.FRONT),
            ((12, 5, 6, 13), vn.FRONT),
            ((13, 6, 7, 10), vn.FRONT),
            ((14, 2, 1, 15), vn.FRONT),
            ((15, 1, 4, 16), vn.FRONT),
            ((16, 4, 5, 12), vn.FRONT),
            ((17, 9, 2), vn.FRONT),
            ((17, 2, 14), vn.FRONT),
            ((18, 14, 15), vn.FRONT),
            ((18, 15, 16), vn.FRONT),
            ((18, 16, 12), vn.FRONT),
            ((18, 12, 13), vn.FRONT),
            ((18, 13, 10), vn.FRONT),
            ((18, 10, 11), vn.FRONT),
            ((18, 11, 17), vn.FRONT),
            ((18, 17, 14), vn.FRONT),
            ((11, 8, 9, 17), vn.FRONT),
        ],
        smooth=True,
        mtl="white",
    )
