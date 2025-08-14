from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Smart City AI Dashboard"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/smartcity"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ML Models
    MODEL_PATH: str = "../ml-models"
    
    # External APIs
    WEATHER_API_KEY: Optional[str] = None
    TRAFFIC_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()