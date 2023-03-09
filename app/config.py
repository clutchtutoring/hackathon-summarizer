from pydantic import BaseSettings

class Settings(BaseSettings):
    """Settings for the app."""
    app_name: str = "Summarizer API"
    redis_url: str = "redis://localhost:6379"
