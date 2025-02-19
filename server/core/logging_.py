import logging
import sys


def configure_logging(
    date_format: str,
    log_format: str,
) -> None:
    """Configure logging from this project."""
    logging.basicConfig(
        datefmt=date_format,
        format=log_format,
        level=logging.INFO,
        handlers=(logging.StreamHandler(sys.stdout),),
    )
