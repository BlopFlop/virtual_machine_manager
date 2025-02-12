import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(
    log_dir: Path,
    name_app: str,
    date_format: str,
    log_format: str,
) -> None:
    """Configure logging from this project."""
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{name_app}.log"
    rotating_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
    logging.basicConfig(
        datefmt=date_format,
        format=log_format,
        level=logging.WARNING,
        handlers=(rotating_handler, logging.StreamHandler()),
    )
