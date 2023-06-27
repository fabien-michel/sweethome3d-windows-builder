from pathlib import Path

materials = {}

for mtl_file in Path("materials/").glob("*.mtl"):
    mtl_lines = []
    mtl_name = ""
    for line in mtl_file.read_text().split("\n"):
        if line.startswith("#"):
            continue
        if line.startswith("newmtl "):
            if mtl_name:
                materials[mtl_name] = "\n".join(mtl_lines)
            mtl_name = line.split(" ")[1]
            mtl_lines = [line]
        elif mtl_name and line:
            mtl_lines.append(line)

    if mtl_name and mtl_lines:
        materials[mtl_name] = "\n".join(mtl_lines)
