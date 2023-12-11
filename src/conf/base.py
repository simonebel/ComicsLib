import os
from pathlib import Path

BASE_DIR = Path(os.environ["BASE_DIR"])
DATA_DIR = os.environ["DATA_DIR"]
SQLITE_DIR = os.environ["SQLITE_DIR"]
SQLITE_DB = "comics.db"

IMAGE_FOLDER = Path(BASE_DIR, "front", "public", "static", "img")
