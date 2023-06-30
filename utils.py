import logging
import re
from collections import defaultdict

from config import LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

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
