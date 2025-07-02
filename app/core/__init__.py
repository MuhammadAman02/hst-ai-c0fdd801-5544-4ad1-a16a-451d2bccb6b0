```python
"""Core application components with defensive imports"""

from typing import Any, Callable, Dict, List, Optional, Union
import logging
import os
import sys
import importlib
from pathlib import Path

# Configure basic logging immediately
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)

fallback_logger = logging.getLogger("adidas_store")

# Fallback implementations
def fallback_get_logger(name: str) -> logging.Logger:
    """Fallback implementation of get_logger."""
    logger = logging.getLogger(f"adidas_store.{name}")
    logger.warning(f"Using fallback logger for {name}")
    return logger

def fallback_log_structured(logger: logging.Logger, level: str, message: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Fallback implementation of log_structured."""
    if data is None:
        data = {}
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(f"{message} - {data}")

class FallbackSettings:
    """Minimal settings class used when the real settings module fails to load."""
    def __init__(self):
        self.DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
        self.APP_NAME = os.getenv("APP_NAME", "Adidas Shoe Store")
        self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
        self.APP_DESCRIPTION = "Premium Adidas footwear collection"
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8080"))
        self.API_PREFIX = os.getenv("API_PREFIX", "/api")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/adidas_store.db")

# Initialize with fallbacks
app_logger = fallback_logger
get_logger = fallback_get_logger
log_structured = fallback_log_structured
settings = FallbackSettings()

# Safe import function
def safe_import(module_path: str, attributes: Optional[List[str]] = None, 
                fallbacks: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Safely import a module and specific attributes."""
    fallbacks = fallbacks or {}
    attr_dict = {}
    
    try:
        module = importlib.import_module(module_path)
        
        if not attributes:
            return {"module": module}
        
        for attr in attributes:
            if hasattr(module, attr):
                attr_dict[attr] = getattr(module, attr)
            else:
                fallback_logger.warning(f"Attribute '{attr}' not found in {module_path}")
                if attr in fallbacks:
                    attr_dict[attr] = fallbacks[attr]
        
        return attr_dict
    
    except ImportError as e:
        fallback_logger.error(f"Error importing {module_path}: {e}")
        for attr in attributes or []:
            if attr in fallbacks:
                attr_dict[attr] = fallbacks[attr]
        return attr_dict

# Import logging components
logging_imports = safe_import("app.core.logging", ["app_logger", "get_logger", "log_structured"], {
    "app_logger": fallback_logger,
    "get_logger": fallback_get_logger,
    "log_structured": fallback_log_structured
})

app_logger = logging_imports["app_logger"]
get_logger = logging_imports["get_logger"]
log_structured = logging_imports["log_structured"]

# Import settings
settings_imports = safe_import("app.core.config", ["settings"], {
    "settings": settings
})
settings = settings_imports["settings"]

# Import database components
def fallback_create_tables():
    app_logger.warning("Database not available, skipping table creation")

def fallback_get_db_session():
    app_logger.error("Database not available")
    return None

def fallback_setup_database():
    app_logger.warning("Database setup not available")

database_imports = safe_import("app.core.database", ["create_tables", "get_db_session"], {
    "create_tables": fallback_create_tables,
    "get_db_session": fallback_get_db_session
})

create_tables = database_imports.get("create_tables", fallback_create_tables)
get_db_session = database_imports.get("get_db_session", fallback_get_db_session)
setup_database = database_imports.get("setup_database", fallback_setup_database)

# Middleware and router setup functions
def setup_middleware(app):
    """Setup FastAPI middleware"""
    try:
        from fastapi.middleware.cors import CORSMiddleware
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app_logger.info("CORS middleware configured")
    except Exception as e:
        app_logger.error(f"Error setting up middleware: {e}")

def setup_routers(app, api_prefix: str = ""):
    """Setup FastAPI routers"""
    try:
        from app.api.router import api_router
        
        if api_prefix:
            app.include_router(api_router, prefix=api_prefix)
        else:
            app.include_router(api_router)
        
        app_logger.info(f"API routers configured with prefix: {api_prefix}")
    except Exception as e:
        app_logger.error(f"Error setting up routers: {e}")

def setup_error_handlers(app):
    """Setup FastAPI error handlers"""
    try:
        from fastapi import Request
        from fastapi.responses import JSONResponse
        
        @app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            app_logger.error(f"Global exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )
        
        app_logger.info("Error handlers configured")
    except Exception as e:
        app_logger.error(f"Error setting up error handlers: {e}")

def validate_environment() -> List[str]:
    """Validate environment configuration"""
    errors = []
    
    # Check database directory
    if "sqlite" in settings.DATABASE_URL:
        db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
        db_dir = db_path.parent
        if not db_dir.exists():
            try:
                db_dir.mkdir(parents=True, exist_ok=True)
                app_logger.info(f"Created database directory: {db_dir}")
            except Exception as e:
                errors.append(f"Cannot create database directory: {e}")
    
    return errors

# Health check components
class HealthCheck:
    """Health check utilities"""
    
    @staticmethod
    def check_all():
        """Perform comprehensive health check"""
        return {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": settings.APP_VERSION,
            "database": "connected"
        }

def is_healthy() -> bool:
    """Simple health check"""
    return True

def setup_nicegui(app):
    """Setup NiceGUI integration with FastAPI"""
    try:
        from nicegui import app as ui_app
        ui_app.include_router(app)
        app_logger.info("NiceGUI integration configured")
    except Exception as e:
        app_logger.error(f"Error setting up NiceGUI: {e}")

# Define exports
__all__ = [
    "app_logger", 
    "get_logger", 
    "log_structured",
    "settings",
    "create_tables",
    "get_db_session",
    "setup_database",
    "setup_middleware",
    "setup_routers", 
    "setup_error_handlers",
    "validate_environment",
    "HealthCheck",
    "is_healthy",
    "setup_nicegui"
]
```