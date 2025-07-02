```python
"""Application configuration using Pydantic settings"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = Field(default="Adidas Shoe Store")
    APP_DESCRIPTION: str = Field(default="Premium Adidas footwear collection")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8080)
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/adidas_store.db")
    
    # Security
    SECRET_KEY: str = Field(default="adidas-store-secret-key-change-in-production")
    
    # API
    API_PREFIX: str = Field(default="/api")
    
    # File uploads
    UPLOAD_DIRECTORY: str = Field(default="./app/static/uploads")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: Optional[str] = Field(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Ensure data directory exists
        if "sqlite" in self.DATABASE_URL:
            db_path = Path(self.DATABASE_URL.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure upload directory exists
        Path(self.UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Create global settings instance
settings = Settings()
```