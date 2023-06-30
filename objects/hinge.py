from obj_types.part import Part
from objects.cylinder import new_cylinder


def new_hinge(
    x=0,
    y=0,
    z=0,
    diameter=1.0,
    height=5.0,
    pane_index=None,
    hinge_index=None,
    mtl="white",
):
    name = f"sweethome3d_hinge_{pane_index}_{hinge_index}"
    return new_cylinder(
        x=x, y=y, z=z, diameter=diameter, height=height, name=name, mtl=mtl
    )
