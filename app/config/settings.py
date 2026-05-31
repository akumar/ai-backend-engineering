from pydantic import BaseModel, AnyUrl
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()


# Read raw environment values with sensible defaults
_SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
_ALGORITHM = os.getenv("ALGORITHM", "HS256")
_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class Settings(BaseModel):
    app_name: str = "My App"
    debug: bool = False
    secret_key: str = _SECRET_KEY
    algorithm: str = _ALGORITHM
    access_token_expire_minutes: int = _ACCESS_TOKEN_EXPIRE_MINUTES
    database_url: Optional[AnyUrl] = None
    allowed_hosts: List[str] = ["*"]
    log_level: str = "INFO"


# Singleton settings instance created from environment
settings = Settings()


def get_settings() -> Settings:
    return settings
