import logging
from logging.handlers import RotatingFileHandler
import os


def configure_logging(app) -> None:
    log_level_name = app.config.get("LOG_LEVEL", "INFO")
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)
    app.logger.setLevel(log_level)

    log_file = app.config.get("LOG_FILE", "./logs/app.log")
    log_dir = os.path.dirname(log_file) or "."
    os.makedirs(log_dir, exist_ok=True)

    handler = RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=3)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)

    if not any(isinstance(h, RotatingFileHandler) for h in app.logger.handlers):
        app.logger.addHandler(handler)
