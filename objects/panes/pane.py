from obj_types.sash import Sash
from obj_types.thickness import Thickness
from obj_types.part import Part
from objects.panes.double_opening_pane import new_double_opening_pane
from objects.panes.fixed_pane import new_fixed_pane
from objects.panes.single_opening_pane import new_single_opening_pane


def new_pane(
    index=1,
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
    hinges_count=3,
    type="fixed",
    opening_pane_index=1,
) -> tuple[list[Part], list[Sash] | None]:
    if not outer_frame_thickness:
        outer_frame_thickness = frame_thickness
    if not outer_frame_depth:
        outer_frame_depth = depth

    if type == "fixed":
        return new_fixed_pane(
            index=index,
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
        return new_single_opening_pane(
            index=index,
            direction=type.split("-")[1],
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
            opening_pane_index=opening_pane_index,
        )
    elif type == "opening-double":
        return new_double_opening_pane(
            index=index,
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
            opening_pane_index=opening_pane_index,
        )
    return [], []
