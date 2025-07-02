```python
"""NiceGUI integration setup for FastAPI"""

from typing import Optional
from app.core.logging import get_logger

logger = get_logger(__name__)

def setup_nicegui(fastapi_app) -> None:
    """Setup NiceGUI integration with FastAPI app"""
    try:
        from nicegui import app as nicegui_app
        
        # Mount FastAPI app with NiceGUI
        nicegui_app.include_router(fastapi_app)
        
        logger.info("NiceGUI integration with FastAPI configured successfully")
        
    except ImportError as e:
        logger.error(f"NiceGUI not available: {e}")
        raise
    except Exception as e:
        logger.error(f"Error setting up NiceGUI integration: {e}")
        raise

def configure_nicegui_settings(
    title: str = "Adidas Shoe Store",
    favicon: Optional[str] = None,
    dark: Optional[bool] = None
) -> None:
    """Configure NiceGUI global settings"""
    try:
        from nicegui import app as nicegui_app
        
        # Configure app settings
        if title:
            nicegui_app.title = title
        
        if favicon:
            nicegui_app.favicon = favicon
            
        if dark is not None:
            nicegui_app.dark = dark
        
        logger.info(f"NiceGUI settings configured: title='{title}'")
        
    except ImportError:
        logger.warning("NiceGUI not available for configuration")
    except Exception as e:
        logger.error(f"Error configuring NiceGUI settings: {e}")
```