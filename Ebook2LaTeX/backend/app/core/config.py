"""
Core application configuration using Pydantic Settings.
Values are loaded from environment variables / .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    APP_NAME: str = "Ebook2LaTeX"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # CORS – comma-separated origins, e.g. "http://localhost:5173,http://localhost:3000"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Database (intentionally not connected in Phase 1)
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/ebook2latex"

    # File upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    UPLOAD_DIR: str = "uploads"


settings = Settings()
