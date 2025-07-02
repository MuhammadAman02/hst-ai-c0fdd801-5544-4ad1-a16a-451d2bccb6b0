```python
"""Logging configuration for the application"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
from pathlib import Path

# Define exports at the top
__all__ = ["app_logger", "get_logger", "log_structured"]

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger for the application
app_logger = logging.getLogger("adidas_store")
app_logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
app_logger.addHandler(console_handler)

# Create a file handler if LOG_FILE is set in environment
log_file = os.getenv("LOG_FILE")
if log_file:
    try:
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        if log_dir and not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a rotating file handler (10 MB max size, keep 5 backup files)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)
    except Exception as e:
        app_logger.error(f"Failed to set up file logging: {e}")

# Set log level from environment variable if provided
try:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    if log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        app_logger.setLevel(getattr(logging, log_level))
    else:
        app_logger.warning(f"Invalid log level: {log_level}, using INFO")
        app_logger.setLevel(logging.INFO)
except Exception as e:
    app_logger.error(f"Error setting log level: {e}, using INFO")
    app_logger.setLevel(logging.INFO)

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Create a logger for a specific module.
    
    Args:
        name: The name of the module (typically __name__)
        level: Optional log level override
        
    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level from parameter or environment
    try:
        if level and level.upper() in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            logger.setLevel(getattr(logging, level.upper()))
        else:
            logger.setLevel(app_logger.level)
    except Exception as e:
        app_logger.error(f"Error setting log level for {name}: {e}")
        logger.setLevel(logging.INFO)
    
    # Add handlers if not already present
    if not logger.handlers:
        # Add console handler
        logger.addHandler(console_handler)
        
        # Add file handler if available
        if log_file and 'file_handler' in locals():
            logger.addHandler(file_handler)
    
    return logger

def log_structured(logger: logging.Logger, level: str, message: str, data: Dict[str, Any]) -> None:
    """Log a message with structured data.
    
    Args:
        logger: The logger instance
        level: The log level (debug, info, warning, error, critical)
        message: The log message
        data: Dictionary of structured data to include
    """
    try:
        if level.lower() == "debug":
            logger.debug(f"{message} - {data}")
        elif level.lower() == "info":
            logger.info(f"{message} - {data}")
        elif level.lower() == "warning":
            logger.warning(f"{message} - {data}")
        elif level.lower() == "error":
            logger.error(f"{message} - {data}")
        elif level.lower() == "critical":
            logger.critical(f"{message} - {data}")
        else:
            logger.info(f"{message} - {data} (unknown level: {level})")
    except Exception as e:
        logger.error(f"Error in log_structured: {e}")
        logger.error(f"{message} - {data}")

# Re-define exports at the end
__all__ = ["app_logger", "get_logger", "log_structured"]
```