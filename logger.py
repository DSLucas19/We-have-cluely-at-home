"""Logging configuration for AI Assistant application."""
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "ai_assistant", log_level: str = "INFO", save_logs: bool = True) -> logging.Logger:
    """Set up application logger.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        save_logs: Whether to save logs to file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if save_logs:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_dir / "ai_assistant.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()
