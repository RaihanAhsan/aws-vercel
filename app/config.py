from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True
    TIMEZONE: str = "Asia/Jakarta"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()