"""Structured logging configuration for cstudio CLI."""

import logging
import os

import structlog


def configure_logging(log_level: str | None = None) -> None:
    """Configure structlog with human-readable console output.

    Args:
        log_level: Override log level. Falls back to LOG_LEVEL env var, then INFO.
    """
    level_name = log_level or os.environ.get("LOG_LEVEL", "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)

    # Configure stdlib logging (structlog wraps it)
    logging.basicConfig(format="%(message)s", level=level, force=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer(
                colors=True,
                pad_event=30,
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
