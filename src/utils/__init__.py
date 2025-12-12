import logging
import sys
from loguru import logger as loguru_logger
from pathlib import Path

# Remove default handler
loguru_logger.remove()

def setup_logger(
    name: str = "ds-project",
    level: str = "INFO",
    log_file: str | None = None,
) -> None:
    """
    Configure Loguru logger with beautiful, colored output + optional file logging.
    Used across the entire project.
    """
    format_str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # Console handler (always)
    loguru_logger.add(
        sys.stderr,
        format=format_str,
        level=level.upper(),
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Optional file handler
    if log_file:
        log_file_path = Path("logs") / log_file
        log_file_path.parent.mkdir(exist_ok=True)
        loguru_logger.add(
            log_file_path,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            level=level.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )

    # Replace standard logging with Loguru (so pandas, sqlalchemy, etc. use it too)
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            level = loguru_logger.level(record.levelname).name
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            loguru_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

# Auto-setup on import (most convenient for notebooks + scripts)
setup_logger(level="INFO")

# Export a pre-configured logger
logger = loguru_logger

# Example usage:
# from src.utils import logger
# logger.info("Training started")
# logger.error("Something went wrong", exc_info=True)
