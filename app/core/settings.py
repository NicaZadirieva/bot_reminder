from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: str = Field(default="default_token", validation_alias="BOT_TOKEN")

    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./reminder_bot.db", validation_alias="DATABASE_URL"
    )

    # Environment
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")
    ENVIRONMENT: str = Field(default="development", validation_alias="ENVIRONMENT")
    TIMEZONE: str = Field(default="UTC", validation_alias="TIMEZONE")
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Настройки для загрузки из .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # игнорировать лишние переменные окружения
    )


# Создаём единственный экземпляр конфигурации
settings = Settings()
