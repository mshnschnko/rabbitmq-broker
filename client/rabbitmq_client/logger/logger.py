import logging
import logging.config

from log_config import LogConfig


class Logger:
    __log_config = LogConfig()
    __logger: logging.Logger = None

    def __new__(cls) -> 'Logger':
        if cls.__logger is None:
            cls.__logger = super().__new__(cls)
        return cls.__logger

    def __init__(self) -> None:
        self.__logger = self.__get_logger(self.__log_config.logger_name)

    def __get_file_handler(self):
        file_handler = logging.FileHandler(self.__log_config.filename)
        file_handler.setLevel(self.__log_config.file_level)
        file_handler.setFormatter(logging.Formatter(self.__log_config.format))
        return file_handler

    def __get_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.__log_config.console_level)
        stream_handler.setFormatter(logging.Formatter(self.__log_config.format))
        return stream_handler

    def __get_logger(self, logger_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        logger.setLevel(self.__log_config.level)
        if not logger.hasHandlers():
            logger.addHandler(self.__get_file_handler())
            logger.addHandler(self.__get_stream_handler())
        return logger

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def warning(self, message: str) -> None:
        self.__logger.warning(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def update_config(self) -> None:
        self.__logger = self.__get_logger(self.__log_config.logger_name)