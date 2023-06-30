from obj_types.part import Part
from objects.hinge import new_hinge


def new_pane_hinges(
    opening_pane_index,
    x,
    y,
    z,
    diameter,
    hinge_height,
    pane_height,
    count,
    max_height_ratio=0.9,
) -> list[Part]:
    count = max(count, 2)
    max_height = pane_height * max_height_ratio
    start_y = y + pane_height * ((1 - max_height_ratio) / 2) - hinge_height / 2

    parts = []
    for index in range(0, count):
        parts.append(
            new_hinge(
                diameter=diameter,
                height=hinge_height,
                pane_index=opening_pane_index,
                hinge_index=index + 1,
                x=x,
                y=start_y + (max_height / (count - 1)) * index,
                z=z,
            )
        )

    return parts
