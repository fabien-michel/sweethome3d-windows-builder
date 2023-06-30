from obj_types.part import Part
from obj_types.sash import Sash
from obj_types.thickness import Thickness
from objects.frame import new_frame
from objects.panes.frame_with_glass import new_frame_with_glass
from objects.panes.pane_hinges import new_pane_hinges


def new_double_opening_pane(
    index=1,
    opening="left",
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

    # if opening == "left":
    left_opening_frame_x = x + delta_left
    left_opening_frame_y = y + delta_bottom
    left_opening_frame_z = z + depth
    left_opening_frame_width = (width - delta_left - delta_right) / 2
    left_opening_frame_height = height - delta_bottom - delta_top
    left_hinge_x = left_opening_frame_x - 1
    left_sash_x = left_opening_frame_x
    left_sash_z = left_opening_frame_z
    # elif opening == "right":
    right_opening_frame_x = x + delta_left + left_opening_frame_width
    right_opening_frame_y = y + delta_bottom
    right_opening_frame_z = z + outer_frame_depth
    right_opening_frame_width = (width - delta_left - delta_right) / 2
    right_opening_frame_height = height - delta_bottom - delta_top
    right_hinge_x = right_opening_frame_x + right_opening_frame_width
    right_sash_x = right_opening_frame_x + right_opening_frame_width
    right_sash_z = z + outer_frame_depth

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
            x=left_opening_frame_x,
            y=left_opening_frame_y,
            z=left_opening_frame_z,
            height=left_opening_frame_height,
            width=left_opening_frame_width,
            depth=depth,
            thickness=frame_thickness,
            glass_depth=glass_depth,
        ),
        *new_pane_hinges(
            opening_pane_index=opening_pane_index,
            diameter=1,
            hinge_height=5,
            x=left_hinge_x,
            y=left_opening_frame_y,
            z=left_opening_frame_z,
            pane_height=left_opening_frame_height,
            count=hinges_count,
        ),
        *new_frame_with_glass(
            pane_index=index,
            opening=True,
            opening_pane_index=opening_pane_index + 1,
            x=right_opening_frame_x,
            y=right_opening_frame_y,
            z=right_opening_frame_z,
            height=right_opening_frame_height,
            width=right_opening_frame_width,
            depth=depth,
            thickness=frame_thickness,
            glass_depth=glass_depth,
        ),
        *new_pane_hinges(
            opening_pane_index=opening_pane_index + 1,
            diameter=1,
            hinge_height=5,
            x=right_hinge_x,
            y=right_opening_frame_y,
            z=right_opening_frame_z,
            pane_height=right_opening_frame_height,
            count=hinges_count,
        ),
    ]

    sashes = [
        Sash(
            x_axis=left_sash_x,
            z_axis=left_sash_z,
            width=left_opening_frame_width,
        ),
        Sash(
            x_axis=right_sash_x,
            z_axis=right_sash_z,
            width=right_opening_frame_width,
        ),
    ]

    return parts, sashes
