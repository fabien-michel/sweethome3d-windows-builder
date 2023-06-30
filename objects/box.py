from obj_types.part import Part


def new_box(x=0, y=0, z=0, width=1, height=1, depth=0.1, name="box", mtl="white"):
    return Part(
        name=name,
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
            (1, 2, 3, 4),
            (5, 6, 7, 8),
            (1, 2, 6, 5),
            (1, 5, 8, 4),
            (2, 3, 7, 6),
            (3, 4, 8, 7),
        ],
        smooth=False,
        mtl=mtl,
    )
