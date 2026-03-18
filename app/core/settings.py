from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    BOT_TOKEN: str = Field(
        ..., min_length=10, description="Bot token from @BotFather or from VK_API"
    )
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"
    LOG_LEVEL: str = "INFO"


class DatabaseSettings(BaseModel):
    DATABASE_URL: str = Field(..., min_length=10, description="Database connection URL")

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if parsed.scheme not in {"postgresql", "postgresql+asyncpg"}:
            raise ValueError(
                "Database_url scheme must be postgresql or postgresql+asyncpg"
            )
        if not parsed.hostname:
            raise ValueError("Database_url must include hostname")

        dbname = (parsed.path or "").lstrip("/")
        if not dbname:
            raise ValueError("Database_url must include database")

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("Database_url port must be 1...65535")

        return v


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., min_length=10)
    DATABASE_URL: str = Field(..., min_length=10)
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_v = v.upper()
        if upper_v not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return upper_v

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


settings = Settings()  # type:ignore[call-arg]
