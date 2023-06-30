from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import zipfile
from obj_types.window import Window
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import DIST_PATH
CATALOG_FILE_PATH = DIST_PATH / "PluginFurnitureCatalog.properties"


@dataclass
class Library:
    id: str = "LibraryId"
    name: str = "Library"
    description: str = ""
    license: str = ""
    creator: str = ""
    provider: str = ""
    version: str = "1.0"
    json_file_path: Path = None

    windows: list[Window] = field(default_factory=lambda: [])

    @property
    def sh3f_file_path(self):
        return DIST_PATH / f"{self.id}.sh3f"

    def add_window(self, window: Window):
        self.windows.append(window)

    def build_sh3f(self):
        self.build_windows_files()
        self.increment_version()
        self.build_catalog()
        self.build_archive()

    def build_windows_files(self):
        for window in self.windows:
            window.write_files()

    def build_catalog(self):
        env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
        template = env.get_template("catalog.jinja")
        Path(CATALOG_FILE_PATH).write_text(
            template.render(
                generation_date=datetime.now(),
                library=self
                # download_base_url=f"https://github.com/fabien-michel/sweethome3d-textures-ambientcg/raw/{git_tag}",
                # preview_base_url=f"https://raw.githubusercontent.com/fabien-michel/sweethome3d-textures-ambientcg/{git_tag}/previews",
                # version=version,
                # catalog_data=catalog_data,
                # git_tag=git_tag,
                # preview_categories=preview_categories,
                # download_versions=[
                #     (get_package_path(size), DOWNLOAD_URLS[size]) for size in SIZES
                # ],
            )
        )

    def build_archive(self):
        if self.sh3f_file_path.exists():
            self.sh3f_file_path.unlink()
        with zipfile.ZipFile(
            self.sh3f_file_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zip_object:
            zip_object.write(CATALOG_FILE_PATH, CATALOG_FILE_PATH.name)
            for window in self.windows:
                zip_object.write(window.obj_file_path, window.obj_file_archive_path)
                zip_object.write(window.mtl_file_path, window.mtl_file_archive_path)
                zip_object.write(window.icon_file_path, window.icon_file_archive_path)

    def get_incremented_version(self):
        nums = self.version.split(".")
        if len(nums) < 3:
            nums.extend(["0"] * (3 - len(nums)))
        nums = [int(num) for num in nums]
        nums[-1] += 1
        return ".".join(str(num) for num in nums)

    def increment_version(self):
        new_version = self.get_incremented_version()
        if self.json_file_path:
            with self.json_file_path.open("r") as library_json_file:
                json_data = json.load(library_json_file)

            json_data["version"] = new_version

            with self.json_file_path.open("w") as library_json_file:
                json.dump(json_data, library_json_file, indent=2)
        self.version = new_version
        return new_version

    @classmethod
    def from_json_file(cls, json_file_path: Path):
        with json_file_path.open() as library_json_file:
            library_data = json.load(library_json_file)

        library = cls(
            json_file_path=json_file_path,
            id=library_data.get("id", "Library"),
            name=library_data.get("name", "Library"),
            description=library_data.get("description", ""),
            license=library_data.get("license", ""),
            creator=library_data.get("creator", ""),
            provider=library_data.get("provider", ""),
            version=library_data.get("version", "1.0"),
        )
        for window_data in library_data.get("windows", []):
            window = Window.build_from_json(window_data)
            library.add_window(window)

        return library
