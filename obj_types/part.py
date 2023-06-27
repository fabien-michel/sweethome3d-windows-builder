from dataclasses import dataclass, field


@dataclass
class Part:
    name: str = ""
    vertices: list[tuple[float]] = field(default_factory=lambda: [])
    faces: list[tuple[int]] = field(default_factory=lambda: [])
    mtl: str = "white"
    smooth: bool = False

    def get_obj_content(self, vertices_index: int = 0, vertex_normals: dict = None):
        faces = []
        new_vns = []
        for face_pts, vn in self.faces:
            face_pts = tuple(face_pt + vertices_index for face_pt in face_pts)
            vn_idx = None
            if vertex_normals is not None:
                vn_idx = vertex_normals.get(vn)
                if vn_idx is None:
                    vn_idx = len(vertex_normals) + 1
                    vertex_normals[vn] = vn_idx
                    new_vns.append(vn)

            faces.append((face_pts, vn_idx))

        # self.vertices.extend(vertices)
        lines = [f"g {self.name}"]
        lines += [
            "v " + format_vertice_pts(vertice_pts) for vertice_pts in self.vertices
        ]
        lines += [f"usemtl {self.mtl}"]
        lines += ["vn " + " ".join(map(str, vn)) for vn in new_vns]
        lines += [f"s {1 if self.smooth else 'off'}"]
        lines += ["f " + format_face(face) for face in faces]
        return "\n".join(lines)


def format_vertice_pts(vertice_pts) -> str:
    return " ".join(tuple(str(round(vertice_pt, 3)) for vertice_pt in vertice_pts))


def format_face(face) -> str:
    face_pts, vn_idx = face
    if vn_idx:
        return " ".join(tuple(f"{face_pt}//{vn_idx}" for face_pt in face_pts))
    return " ".join(tuple(f"{face_pt}" for face_pt in face_pts))
