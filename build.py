import argparse
from pathlib import Path

from obj_types.library import Library

# LIBRARY_JSON = Path("library.json")


def main(windows_json: Path, *args, **kwargs):
    library = Library.from_json_file(windows_json)
    library.build_sh3f()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python build.py",
        description="Create a SweetHome3D library of windows and doors",
    )
    parser.add_argument("library_json_path", help="json file describing the windows")
    args = parser.parse_args()

    main(Path(args.library_json_path))
