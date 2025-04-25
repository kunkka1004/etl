# logger_config.py
import logging
import os
from pathlib import Path

DEFAULT_LOG_PATH = Path(__file__).resolve().parent.parent / 'logs/etl.log'


class LoggerConfig:
    def __init__(self, level=logging.INFO, log_path=DEFAULT_LOG_PATH):
        self.log_path = log_path
        self.level = level
        self.format = '%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(funcName)s:%(lineno)d - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self._initialized_loggers = set()
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def get_logger(self, name: str) -> logging.Logger:
        if name in self._initialized_loggers:
            return logging.getLogger(name)

        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        if not logger.handlers:

            file_handler = logging.FileHandler(self.log_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(self.format, self.date_format))

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(self.format, self.date_format))

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        return logger