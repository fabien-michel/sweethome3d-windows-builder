from obj_types.part import Part
from obj_types.sash import Sash
from obj_types.thickness import Thickness
from objects.frame import new_frame
from objects.panes.frame_with_glass import new_frame_with_glass
from objects.panes.pane_hinges import new_pane_hinges


def new_single_opening_pane(
    index=1,
    direction="left",
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=5,
    frame_thickness: Thickness = Thickness(5),
    outer_frame_thickness: Thickness | None = None,
    outer_frame_depth=None,
    glass_depth=0.4,
    overlap_outer_frame: Thickness = Thickness(0.5),
    hinges_count=2,
    opening_pane_index=1,
) -> tuple[list[Part], list[Sash]]:
    delta_top = outer_frame_thickness.top * overlap_outer_frame.top
    delta_right = outer_frame_thickness.right * overlap_outer_frame.right
    delta_bottom = outer_frame_thickness.bottom * overlap_outer_frame.bottom
    delta_left = outer_frame_thickness.left * overlap_outer_frame.left

    if direction == "left":
        opening_frame_x = x + delta_left
        opening_frame_y = y + delta_bottom
        opening_frame_z = z + depth
        opening_frame_width = width - delta_left - delta_right
        opening_frame_height = height - delta_bottom - delta_top
        hinge_x = opening_frame_x - 1
        sash_x = opening_frame_x
        sash_z = opening_frame_z
    elif direction == "right":
        opening_frame_x = x + delta_left
        opening_frame_y = y + delta_bottom
        opening_frame_z = z + outer_frame_depth
        opening_frame_width = width - delta_left - delta_right
        opening_frame_height = height - delta_bottom - delta_top
        hinge_x = opening_frame_x + opening_frame_width
        sash_x = opening_frame_x + opening_frame_width
        sash_z = z + outer_frame_depth

    parts: list[Part] = [
        new_frame(
            name=f"outer_frame_pane_{index}",
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=outer_frame_depth,
            thickness=outer_frame_thickness,
        ),
        *new_frame_with_glass(
            pane_index=index,
            opening=True,
            opening_pane_index=opening_pane_index,
            x=opening_frame_x,
            y=opening_frame_y,
            z=opening_frame_z,
            height=opening_frame_height,
            width=opening_frame_width,
            depth=depth,
            thickness=frame_thickness,
            glass_depth=glass_depth,
        ),
        *new_pane_hinges(
            opening_pane_index=opening_pane_index,
            diameter=1,
            hinge_height=5,
            x=hinge_x,
            y=opening_frame_y,
            z=opening_frame_z,
            pane_height=opening_frame_height,
            count=hinges_count,
        ),
    ]

    sash = Sash(
        x_axis=sash_x,
        z_axis=sash_z,
        width=opening_frame_width,
    )

    return parts, [sash]
