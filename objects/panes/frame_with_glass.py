from obj_types.part import Part
from obj_types.thickness import Thickness
from objects.frame import new_frame
from objects.glass import new_glass


def new_frame_with_glass(
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=5,
    thickness: Thickness = Thickness(5),
    glass_depth=0.4,
    opening=False,
    pane_index=1,
    opening_pane_index=1,
) -> list[Part]:
    frame_name = (
        f"sweethome3d_opening_on_hinge_{opening_pane_index}"
        if opening
        else f"frame_{pane_index}"
    )
    glass_name = (
        f"sweethome3d_window_pane_on_hinge_{opening_pane_index}"
        if opening
        else f"glass_{pane_index}"
    )
    return [
        new_frame(
            name=frame_name,
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=depth,
            thickness=thickness,
        ),
        new_glass(
            name=glass_name,
            x=x + thickness.left + 0.01,
            y=y + thickness.bottom + 0.01,
            z=z + depth / 2 - glass_depth / 2,
            height=height - thickness.top - thickness.bottom - 0.02,
            width=width - thickness.right - thickness.left - 0.02,
            depth=glass_depth,
        ),
    ]
