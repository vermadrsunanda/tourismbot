"""
Logging configuration for the tourism bot application.
"""
import logging
import logging.handlers
import os
from config.settings import Config


def setup_logger(name, log_level=None):
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (defaults to config setting)
    
    Returns:
        Configured logger instance
    """
    if log_level is None:
        log_level = Config.LOG_LEVEL
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/tourism_bot.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
