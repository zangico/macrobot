import logging
import os

from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

from ..config import settings
from .context import ContextFilter
from .formatter import get_json_formatter, get_stream_formatter


def setup_logger(
    name: str = "app", debug: bool = False, log_dir: str = "logs"
) -> logging.Logger:

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.propagate = False

    fh = ConcurrentTimedRotatingFileHandler(
        log_path, when="midnight", backupCount=7, encoding="utf-8"
    )
    fh.setFormatter(get_json_formatter())
    fh.addFilter(ContextFilter())

    sh = logging.StreamHandler()
    sh.setFormatter(get_stream_formatter())
    sh.addFilter(ContextFilter())

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


logger = setup_logger(settings.APP.NAME, settings.APP.DEBUG)
