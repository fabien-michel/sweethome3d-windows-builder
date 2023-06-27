from obj_types.sash import Sash
from obj_types.thickness import Thickness
from objects.frame import new_frame
from objects.glass import new_glass
from objects.hinge import new_hinge
from obj_types.part import Part


def new_pane(
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=5,
    frame_thickness: Thickness = Thickness(5),
    outer_frame_thickness: Thickness | None = None,
    outer_frame_depth=None,
    overlap_outer_frame: Thickness = Thickness(0.5),
    glass_depth=0.4,
    hinges_count=2,
    type="fixed",
) -> tuple[list[Part], Sash | None]:
    if not outer_frame_thickness:
        outer_frame_thickness = frame_thickness
    if not outer_frame_depth:
        outer_frame_depth = depth

    if type == "fixed":
        return new_fixed_pane(
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=depth,
            thickness=outer_frame_thickness,
            glass_depth=glass_depth,
        )
    elif type == "opening-left" or type == "opening-right":
        return new_opening_pane(
            opening=type.split("-")[1],
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=depth,
            frame_thickness=frame_thickness,
            outer_frame_thickness=outer_frame_thickness,
            outer_frame_depth=outer_frame_depth,
            glass_depth=glass_depth,
            overlap_outer_frame=overlap_outer_frame,
            hinges_count=hinges_count,
        )
    return [], []

    # if opening:
    #     pass
    # else:
    #     parts += [
    #         *new_frame_with_glass(
    #             x=x,
    #             y=y,
    #             z=z,
    #             height=height,
    #             width=width,
    #             depth=depth,
    #             thickness=outer_frame_thickness,
    #             glass_depth=glass_depth,
    #         )
    #     ]
    # return parts


def new_fixed_pane(
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=5,
    thickness: Thickness | None = None,
    glass_depth=0.4,
) -> tuple[list[Part], list[Sash]]:
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
        ),
        None,
    )


def new_opening_pane(
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
) -> tuple[list[Part], Sash]:
    delta_top = outer_frame_thickness.top * overlap_outer_frame.top
    delta_right = outer_frame_thickness.right * overlap_outer_frame.right
    delta_bottom = outer_frame_thickness.bottom * overlap_outer_frame.bottom
    delta_left = outer_frame_thickness.left * overlap_outer_frame.left

    if opening == "left":
        opening_frame_x = x + delta_left
        opening_frame_y = y + delta_bottom
        opening_frame_z = z + depth
        opening_frame_width = width - delta_left - delta_right
        opening_frame_height = height - delta_bottom - delta_top
        hinge_x = opening_frame_x - 1
        sash_x = opening_frame_x
    elif opening == "right":
        opening_frame_x = x + delta_left
        opening_frame_y = y + delta_bottom
        opening_frame_z = z + outer_frame_depth
        opening_frame_width = width - delta_left - delta_right
        opening_frame_height = height - delta_bottom - delta_top
        hinge_x = opening_frame_x + opening_frame_width + 1
        sash_x = opening_frame_x + opening_frame_width

    parts: list[Part] = [
        new_frame(
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=outer_frame_depth,
            thickness=outer_frame_thickness,
        ),
        *new_frame_with_glass(
            x=opening_frame_x,
            y=opening_frame_y,
            z=opening_frame_z,
            height=opening_frame_height,
            width=opening_frame_width,
            depth=depth,
            thickness=frame_thickness,
            glass_depth=glass_depth,
        ),
        *hinges(
            x=hinge_x,
            y=opening_frame_y,
            z=opening_frame_z - 1,
            height=opening_frame_height,
            count=hinges_count,
        ),
    ]

    sash = Sash(
        x_axis=sash_x,
        y_axis=opening_frame_y,
        width=width,
    )

    return parts, sash


def new_frame_with_glass(
    x=0,
    y=0,
    z=0,
    height=100,
    width=100,
    depth=5,
    thickness: Thickness = Thickness(5),
    glass_depth=0.4,
) -> list[Part]:
    return [
        new_frame(
            x=x,
            y=y,
            z=z,
            height=height,
            width=width,
            depth=depth,
            thickness=thickness,
        ),
        new_glass(
            x=x + thickness.left + 0.01,
            y=y + thickness.bottom + 0.01,
            z=z + depth / 2 - glass_depth / 2,
            height=height - thickness.top - thickness.bottom - 0.02,
            width=width - thickness.right - thickness.left - 0.02,
            depth=glass_depth,
        ),
    ]


def hinges(x, y, z, height, count) -> list[Part]:
    parts = []
    if count == 2:
        parts.append(new_hinge(id="1", x=x, y=y + height / 10, z=z))
        parts.append(new_hinge(id="1", x=x, y=y + height / 10 * 9, z=z))
    if count == 3:
        parts.append(new_hinge(id="1", x=x, y=y + height / 10, z=z))
        parts.append(new_hinge(id="1", x=x, y=y + height / 10 * 5, z=z))
        parts.append(new_hinge(id="1", x=x, y=y + height / 10 * 9, z=z))
    if count == 4:
        parts.append(new_hinge(id="1", x=x, y=y + height / 10, z=z))
        parts.append(new_hinge(id="1", x=x, y=y + height / 10 * 3.6, z=z))
        parts.append(new_hinge(id="1", x=x, y=y + height / 10 * 6.3, z=z))
        parts.append(new_hinge(id="1", x=x, y=y + height / 10 * 9, z=z))
    return parts
