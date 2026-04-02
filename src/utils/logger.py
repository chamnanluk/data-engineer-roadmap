"""Simple project logger configuration."""

from __future__ import annotations

import logging
import sys


def get_logger(name: str = "sales_pipeline", level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger instance.

    Reuses existing handlers to avoid duplicate logs in notebook/repl usage.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
