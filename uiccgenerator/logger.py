import logging
from typing import Optional


def set_logger(debug: bool = False) -> None:
    """
    Function sets logger.
    :param debug: if True, debug logging level will be set.
    """

    logging_level = logging.DEBUG if debug else logging.INFO
    logging_format = "[%(asctime)s.%(msecs)03d %(levelname)7s] %(message)s"
    logging_datefmt = "%Y-%m-%d %H:%M:%S"
    logger = logging.getLogger("uicc_generator")
    logger.setLevel(logging_level)

    formatter = logging.Formatter(fmt=logging_format, datefmt=logging_datefmt)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
