from dataclasses import dataclass, field

from objects.vertex_normals import VN


@dataclass
class Part:
    name: str = ""
    vertices: list[tuple[float]] = field(default_factory=lambda: [])
    faces: list[tuple[int] | tuple[tuple[int], VN | None]] = field(
        default_factory=lambda: []
    )
    mtl: str = "white"
    smooth: bool = False

    def get_obj_content(
        self, vertices_index: int = 0, vertex_normals: dict = None
    ) -> str:
        indexed_faces, new_vns = self.get_indexed_faces(vertices_index, vertex_normals)
        # self.vertices.extend(vertices)
        lines = [f"g {self.name}"]
        lines += [
            "v " + format_vertice_pts(vertice_pts) for vertice_pts in self.vertices
        ]
        lines += [f"usemtl {self.mtl}"]
        lines += ["vn " + " ".join(map(str, vn)) for vn in new_vns]
        lines += [f"s {1 if self.smooth else 'off'}"]
        lines += ["f " + format_face(face) for face in indexed_faces]
        return "\n".join(lines)

    @property
    def normilized_faces(self) -> list[tuple[int], VN | None]:
        return [
            (
                (face_data, None)
                if len(face_data) > 2
                else (face_data[0:-1], face_data[-1])
            )
            for face_data in self.faces
        ]

    def get_indexed_faces(
        self, vertices_index: int = 0, vertex_normals: dict = None
    ) -> tuple[list[tuple[tuple[int], int | None]], list[VN]]:
        indexed_faces = []
        new_vns = []
        for face_pts, vn in self.normilized_faces:
            face_pts = tuple(face_pt + vertices_index for face_pt in face_pts)
            # vn_idx = None
            if vn is None or vertex_normals is None:
                indexed_faces.append((face_pts, None))
                continue
            vn_idx = vertex_normals.get(vn)
            if vn_idx is None:
                vn_idx = len(vertex_normals) + 1
                vertex_normals[vn] = vn_idx
                new_vns.append(vn)

            indexed_faces.append((face_pts, vn_idx))
        return indexed_faces, new_vns


def format_vertice_pts(vertice_pts) -> str:
    return " ".join(tuple(str(round(vertice_pt, 3)) for vertice_pt in vertice_pts))


def format_face(face) -> str:
    face_pts, vn_idx = face
    if vn_idx:
        return " ".join(tuple(f"{face_pt}//{vn_idx}" for face_pt in face_pts))
    return " ".join(tuple(f"{face_pt}" for face_pt in face_pts))
