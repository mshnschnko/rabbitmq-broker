import logging
import logging.config

from log_config import FILENAME, FORMAT, FILE_LEVEL, CONSOLE_LEVEL, LEVEL


def get_file_handler():
    file_handler = logging.FileHandler(FILENAME)
    file_handler.setLevel(FILE_LEVEL)
    file_handler.setFormatter(logging.Formatter(FORMAT))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(CONSOLE_LEVEL)
    stream_handler.setFormatter(logging.Formatter(FORMAT))
    return stream_handler

def get_logger(logger_name) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(LEVEL)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
