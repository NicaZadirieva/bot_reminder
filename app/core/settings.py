from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    BOT_TOKEN: str
    # Environment
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"
    LOG_LEVEL: str = "INFO"


class DatabaseSettings(BaseModel):
    DATABASE_URL: str


class Settings(BaseSettings):
    BOT_TOKEN: str

    # Database
    DATABASE_URL: str

    # Environment
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"
    LOG_LEVEL: str = "INFO"

    # Настройки для загрузки из .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # игнорировать лишние переменные окружения
    )

    @property
    def app(self) -> AppSettings:
        return AppSettings(
            BOT_TOKEN=self.BOT_TOKEN,
            DEBUG=self.DEBUG,
            ENVIRONMENT=self.ENVIRONMENT,
            TIMEZONE=self.TIMEZONE,
            LOG_LEVEL=self.LOG_LEVEL,
        )

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(DATABASE_URL=self.DATABASE_URL)


# Создаём единственный экземпляр конфигурации
settings = Settings()  # type:ignore[call-arg]
