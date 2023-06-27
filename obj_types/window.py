from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path

from config import BASE_DIR_PATH
from obj_types.sash import Sash
from obj_types.thickness import Thickness

from objects.pane import new_pane
from utils import get_id

from .part import Part
from objects.frame import new_frame

from materials import materials


@dataclass
class Window:
    id: str = "WindowId"
    name: str = "Window"
    category: str = "Doors and windows"
    width: int = 100
    height: int = 100
    wall_thickness: int = 25
    elevation: int = 85
    parts: list[Part] = field(default_factory=lambda: [])
    sashs: list[Sash] = field(default_factory=lambda: [])

    def add_part(self, part: Part):
        self.parts.append(part)

    def get_obj_content(self):
        vectices_count = 0
        vertex_normals = None
        txt = []
        txt.append(f"# 3D model {self.obj_file_name}")
        txt.append(f"mtllib {self.mtl_file_name}")
        for part in self.parts:
            txt.append(part.get_obj_content(vectices_count, vertex_normals))
            vectices_count += len(part.vertices)

        # for vn in vertex_normals.keys():
        #     if vn:
        #         txt.insert(2, "vn " + " ".join(map(str, vn)))
        txt.append("")  # obj require new line at end
        return "\n".join(txt)

    def get_mtl_content(self):
        txt = f"# 3D model {self.obj_file_name}"
        for mtl_name in self.get_materials_used():
            txt += "\n\n"
            txt += materials.get(mtl_name, "")
        txt += "\n"  # mtl require new line at end
        return txt

    def get_materials_used(self) -> set[str]:
        return set(part.mtl for part in self.parts)

    @classmethod
    def build_from_json(cls, window_data) -> "Window":
        parts = []

        if window_data["frame_thickness"]:
            # Overall window frame
            parts.append(
                new_frame(
                    x=0,
                    y=0,
                    z=0,
                    width=window_data["width"],
                    height=window_data["height"],
                    depth=window_data["wall_thickness"],
                    thickness=Thickness(window_data["frame_thickness"]),
                )
            )
        panes_parts, sashs = build_panes_group(
            window_data,
            delta_x=window_data["frame_thickness"],
            delta_y=window_data["frame_thickness"],
            delta_width=window_data["frame_thickness"] * 2,
            delta_height=window_data["frame_thickness"] * 2,
        )
        parts.extend(panes_parts)

        return Window(
            id=get_id(window_data["name"]),
            name=window_data["name"],
            category=window_data.get("category", "Doors and windows"),
            width=window_data["width"],
            height=window_data["height"],
            wall_thickness=window_data["wall_thickness"],
            elevation=window_data["elevation"],
            parts=parts,
            sashs=sashs,
        )

    @property
    def obj_file_name(self) -> Path:
        return self.id + ".obj"

    @property
    def obj_file_path(self) -> Path:
        return BASE_DIR_PATH / self.obj_file_name

    @property
    def obj_file_archive_path(self) -> Path:
        return f"{self.id}/{self.obj_file_name}"

    @property
    def icon_file_name(self) -> Path:
        return self.id + ".png"

    @property
    def icon_file_path(self) -> Path:
        return BASE_DIR_PATH / self.icon_file_name

    @property
    def icon_file_archive_path(self) -> Path:
        return self.icon_file_name

    @property
    def mtl_file_name(self) -> Path:
        return self.id + ".mtl"

    @property
    def mtl_file_path(self) -> Path:
        return BASE_DIR_PATH / self.mtl_file_name

    @property
    def mtl_file_archive_path(self) -> Path:
        return f"{self.id}/{self.mtl_file_name}"

    @property
    def obj_file_size(self) -> int:
        return self.obj_file_path.stat().st_size

    def write_files(self):
        self.write_obj_file()
        self.write_mtl_file()
        self.write_icon_file()

    def write_obj_file(self) -> Path:
        file_path = self.obj_file_path
        file_path.write_text(self.get_obj_content())
        return file_path

    def write_mtl_file(self) -> Path:
        file_path = self.mtl_file_path
        file_path.write_text(self.get_mtl_content())
        return file_path

    def write_icon_file(self) -> Path:
        import f3d

        f3d.engine.autoloadPlugins()
        eng = f3d.engine(f3d.window.NATIVE_OFFSCREEN)
        options = eng.getOptions()
        window = eng.getWindow()
        camera = window.getCamera()
        options.set("render.effect.ambient-occlusion", True)
        # options.set("render.effect.anti-aliasing", True)
        eng.getLoader().loadScene(str(self.obj_file_path))
        window.setSize(200, 200)
        camera.setPosition(f3d.point3_t(250, 150, 250))
        img = window.renderToImage(True)
        img.save(str(self.icon_file_path))

        # subprocess.run(
        #     [
        #         "f3d",
        #         "--output=" + str(self.icon_file_path),
        #         "--config=./f3dconfig.json",
        #         "--camera-position=250,150,250",
        #         str(self.obj_file_path),
        #     ]
        # )

    @property
    def depth(self) -> float:
        all_vertices = list(chain(*[part.vertices for part in self.parts]))
        all_z = [v[2] for v in all_vertices]
        min_z = min(all_z)
        max_z = max(all_z)
        return max_z - min_z

    def sashs_attr(self, attr_name) -> str:
        return " ".join(str(getattr(sash, attr_name)) for sash in self.sashs)

        # for part in self.parts:
        # part.vertices

    # def view(self):
    #     import f3d

    #     f3d.engine.autoloadPlugins()

    #     eng = f3d.engine(f3d.window.NATIVE)
    #     options = eng.getOptions()
    #     # options.set("model.scivis.array-name", "Normals")
    #     # options.set("model.scivis.component", 0)
    #     # options.set("ui.bar", True)
    #     # options.set("scene.grid", True)
    #     options.set("render.effect.anti-aliasing", True)
    #     options.set("render.effect.ambient-occlusion", True)

    #     file_path = self.write_obj_file()

    #     eng.getLoader().loadGeometry(str(file_path), True)
    #     eng.getInteractor().start()


def build_panes_group(
    group_data: dict, delta_x=0, delta_y=0, delta_width=0, delta_height=0
) -> tuple[list[Part], list[Sash]]:
    parts: list[Part] = []
    sashs: list[Sash] = []
    group_width = group_data["width"] - delta_width
    group_height = group_data["height"] - delta_height
    for pane_data in group_data["panes"]:
        # is_first_pane_of_group = pane_index == 0
        # is_last_pane_of_group = pane_index == len(group_data["panes"]) - 1
        if group_data["dir"] == "h":
            width_pc = pane_data.get("width_pc") or pane_data.get("size_pc")
            height_pc = 1
        elif group_data["dir"] == "v":
            height_pc = pane_data.get("height_pc") or pane_data.get("size_pc")
            width_pc = 1
        pane_width = group_width * width_pc
        pane_height = group_height * height_pc
        pane_z = pane_data.get("z") or group_data.get("pane_z") or 30
        pane_depth = pane_data.get("depth") or group_data.get("pane_depth") or 5
        outer_frame_depth = (
            pane_data.get("outer_frame_depth")
            or group_data.get("pane_outer_frame_depth")
            or pane_depth
        )
        pane_frame_thickness = Thickness(
            pane_data.get("frame_thickness")
            or group_data.get("pane_frame_thickness")
            or 1.5
        )
        outer_frame_thickness = Thickness(
            pane_data.get("outer_frame_thickness")
            or group_data.get("pane_outer_frame_thickness")
            or pane_frame_thickness
        )
        overlap_outer_frame = Thickness(
            pane_data.get("overlap_outer_frame")
            or group_data.get("pane_overlap_outer_frame")
            or 0.5
        )
        glass_thickness = (
            pane_data.get("glass_thickness") or group_data.get("glass_thickness") or 0.4
        )
        type = pane_data.get("type")
        hinges_count = pane_data.get("hinges_count", 2)
        opening_angle_start = pane_data.get("opening_angle_start", 0)
        opening_angle_end = pane_data.get("opening_angle_end", 90)

        pane_parts, pane_sash = new_pane(
            x=delta_x,
            y=delta_y,
            z=pane_z,
            width=pane_width,
            height=pane_height,
            depth=pane_depth,
            frame_thickness=pane_frame_thickness,
            outer_frame_thickness=outer_frame_thickness,
            outer_frame_depth=outer_frame_depth,
            overlap_outer_frame=overlap_outer_frame,
            glass_depth=glass_thickness,
            hinges_count=hinges_count,
            type=type,
        )
        parts.extend(pane_parts)

        if pane_sash:
            pane_sash.start_angle = opening_angle_start
            pane_sash.end_angle = opening_angle_end
            sashs.append(pane_sash)

        match group_data["dir"]:
            case "h":
                delta_x += pane_width
            case "v":
                delta_y += pane_height

    return parts, sashs
