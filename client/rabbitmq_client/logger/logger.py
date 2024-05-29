import logging
import logging.config

from log_config import LogConfig

log_config = LogConfig()

def get_file_handler():
    file_handler = logging.FileHandler(log_config.filename)
    file_handler.setLevel(log_config.file_level)
    file_handler.setFormatter(logging.Formatter(log_config.format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_config.console_level)
    stream_handler.setFormatter(logging.Formatter(log_config.format))
    return stream_handler

def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_config.level)
    if not logger.hasHandlers():
        logger.addHandler(get_file_handler())
        logger.addHandler(get_stream_handler())
    return logger
