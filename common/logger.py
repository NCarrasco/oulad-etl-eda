# logger.py
import logging

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger