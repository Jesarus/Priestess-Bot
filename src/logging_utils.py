"""
Centralized logging utilities for the Discord bot.
Provides consistent logging setup across all modules.
"""

import logging
from typing import Optional
from pathlib import Path

from constants import LOG_FORMAT, LOG_DATE_FORMAT, MAX_LOG_FILE_SIZE, LOG_BACKUP_COUNT
from observability import observability


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with consistent configuration.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger already has handlers, return it
    if logger.handlers:
        return logger
    
    # Set level to DEBUG to capture all messages
    logger.setLevel(logging.DEBUG)
    
    # Don't propagate to root logger to avoid duplicate messages
    logger.propagate = False
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt=LOG_DATE_FORMAT
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler with rotation
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'bot.log',
        maxBytes=MAX_LOG_FILE_SIZE,
        backupCount=LOG_BACKUP_COUNT
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Create error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'errors.log',
        maxBytes=MAX_LOG_FILE_SIZE,
        backupCount=LOG_BACKUP_COUNT
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    logger.addHandler(error_handler)
    
    return logger


def log_with_observability(level: int, message: str, logger: Optional[logging.Logger] = None, **context):
    """
    Log a message with both standard logging and observability system.
    
    Args:
        level: Log level (logging.INFO, logging.ERROR, etc.)
        message: Log message
        logger: Optional logger instance (uses observability logger if None)
        **context: Additional context information
    """
    if logger is None:
        logger = observability.logger.logger
    
    # Log with standard logging
    logger.log(level, message)
    
    # Also log with observability system if available
    if hasattr(observability, 'logger'):
        if level >= logging.ERROR:
            observability.logger.error(message, **context)
        elif level >= logging.WARNING:
            observability.logger.warning(message, **context)
        elif level >= logging.INFO:
            observability.logger.info(message, **context)
        else:
            observability.logger.debug(message, **context)


def setup_logging():
    """Set up logging for the entire application."""
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)  # Only show warnings and errors from root
    
    # Get application logger
    app_logger = get_logger("priestess_bot")
    app_logger.info("Logging system initialized")
    
    return app_logger
