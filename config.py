import logging
from pathlib import Path


DIST_PATH = Path("dist")
DIST_PATH.mkdir(exist_ok=True)
LOG_LEVEL = logging.DEBUG
