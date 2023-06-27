from collections import defaultdict
import re

global_ids = defaultdict(int)


def get_id(prefix=""):
    prefix = re.sub(r"[^\w+]", "", prefix)
    global global_ids
    global_ids[prefix] += 1
    return f"{prefix}_{global_ids[prefix]}"


def normalize_thickness(thickness):
    if isinstance(thickness, (int, float)):
        return thickness, thickness, thickness, thickness

    return thickness
