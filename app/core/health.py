```python
"""Health check endpoints and utilities"""

import time
from typing import Dict, Any
from app.core.logging import get_logger

logger = get_logger(__name__)

class HealthCheck:
    """Health check utilities for the application"""
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """Perform comprehensive health check"""
        try:
            # Basic health check
            health_data = {
                "status": "healthy",
                "timestamp": time.time(),
                "service": "adidas-shoe-store",
                "version": "1.0.0"
            }
            
            # Check database connectivity
            try:
                from app.core.database import get_db_session
                with get_db_session() as db:
                    # Simple query to test database
                    db.execute("SELECT 1")
                    health_data["database"] = "connected"
            except Exception as e:
                logger.warning(f"Database health check failed: {e}")
                health_data["database"] = "disconnected"
                health_data["status"] = "degraded"
            
            # Check if we can import core services
            try:
                from app.services.product_service import ProductService
                from app.services.cart_service import CartService
                health_data["services"] = "available"
            except Exception as e:
                logger.warning(f"Services health check failed: {e}")
                health_data["services"] = "unavailable"
                health_data["status"] = "degraded"
            
            return health_data
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "timestamp": time.time(),
                "error": str(e)
            }

def is_healthy() -> bool:
    """Simple boolean health check"""
    try:
        health_data = HealthCheck.check_all()
        return health_data.get("status") in ["healthy", "degraded"]
    except Exception:
        return False
```