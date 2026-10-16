### Application Configuration -- app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings): # Reads application settings from environment variables and configured environment files.

    DATABASE_URL: str
# Defines the database connection URL
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
## This helps keep credentials and environment-specific configuration outside the application source code

settings = Settings()

