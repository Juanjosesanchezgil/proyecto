import logging
import sys


def setup_logging():
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.formatter(
            "%(levelname)s:      %(asctime)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
