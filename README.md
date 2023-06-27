# Windows builder for SweetHome3D

Help you build windows where you can define many sashes per windows.
It build 3D objects according to your specifications and build a Furniture Library (.sh3f) importable in SweetHome3D.

## Dependencies

- f3d as library with python binding [https://github.com/f3d-app/f3d](https://github.com/f3d-app/f3d)
- python 3.11 (should work with 3.10)
- poetry [https://python-poetry.org](https://python-poetry.org)

## Installation

```
poetry install
```

## Run

Descibe the windows in a json file as descibed below and run:

```
poetry run python build.py mylibrary.json
```

The .sh3f file will be build in `dist/` folder
