from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Summarizer API"
    redis_url: str = "redis://localhost:6379"