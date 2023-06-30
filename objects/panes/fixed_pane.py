from obj_types.part import Part
from obj_types.sash import Sash
from obj_types.thickness import Thickness
from objects.panes.frame_with_glass import new_frame_with_glass


def new_fixed_pane(
    index=1,
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=5,
    thickness: Thickness | None = None,
    glass_depth=0.4,
) -> tuple[list[Part], list]:
    return (
        new_frame_with_glass(
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=depth,
            thickness=thickness,
            glass_depth=glass_depth,
            pane_index=index,
        ),
        [],
    )
