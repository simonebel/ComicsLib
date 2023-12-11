import logging
from datetime import datetime
from pathlib import Path

from conf.base import BASE_DIR

"""
Logger with date time formated
"""

LOG_DIR = Path(BASE_DIR, "logs")


class ColoredFormatter(logging.Formatter):
    NC = "\x1b[0m"
    BBlack = "\x1b[1;30m"
    BRed = "\x1b[1;31m"
    BGreen = "\x1b[1;32m"
    BYellow = "\x1b[1;33m"
    BBlue = "\x1b[1;34m"
    BPurple = "\x1b[1;35m"
    BCyan = "\x1b[1;36m"
    BWhite = "\x1b[1;37m"
    reset = "\x1b[0m"

    format = "%(asctime)s - %(name)s - %(message)s"

    level = "%(levelname)s"
    FORMATS = {
        logging.DEBUG: "[" + BCyan + level + reset + "] " + format,
        logging.INFO: "[" + BBlue + level + reset + "] " + format,
        logging.WARNING: "[" + BYellow + level + reset + "] " + format,
        logging.ERROR: "[" + BRed + level + reset + "] " + format,
        logging.CRITICAL: "[" + BPurple + level + reset + "] " + format,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_log(
    file_name: str,
    overwrite=False,
    disable_stream=False,
    level=logging.INFO,
    redirect_file: str = "",
):
    file_path = Path(file_name)

    posix_parents = file_path.parents
    for idx, posix in enumerate(posix_parents):
        if posix.name == "src":
            src_pos = idx
            feature_name = posix_parents[idx - 1].name

    log_name = f"{'/'.join(reversed([parent.name for (idx, parent) in enumerate(file_path.parents) if idx < src_pos]))}/{file_path.name}"

    now = datetime.now().date()

    module_folders = file_name.split(feature_name)[-1].split("/")[:-1]

    current_module_date_folder = LOG_DIR.joinpath(
        feature_name, str(now), *module_folders
    )
    current_module_date_folder.mkdir(exist_ok=True, parents=True)

    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    full_log_path = Path(
        current_module_date_folder, file_path.name.replace(".py", ".log")
    )
    if overwrite and full_log_path.exists():
        full_log_path.unlink()

    file_handler = logging.FileHandler(full_log_path)
    formatter = logging.Formatter(
        "[%(levelname)s] - %(asctime)s - %(name)s: %(message)s"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    logger.addHandler(file_handler)

    if not disable_stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(ColoredFormatter())
        logger.addHandler(stream_handler)

    if redirect_file:
        redirect_path = LOG_DIR.joinpath(feature_name, str(now), f"{redirect_file}.log")
        redirected_file_handler = logging.FileHandler(redirect_path)
        redirected_file_handler.setFormatter(formatter)
        redirected_file_handler.setLevel(level)

        logger.addHandler(redirected_file_handler)

    return logger
