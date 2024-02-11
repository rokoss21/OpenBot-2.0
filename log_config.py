#log_config.py
import logging
from config import LOG_FILE

def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Проверяем, добавлен ли StreamHandler корневому логгеру
    root_logger = logging.getLogger()
    if not any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers):
        # Добавляем StreamHandler для вывода в консоль, если он ещё не добавлен
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Настроить при необходимости
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

setup_logging()
