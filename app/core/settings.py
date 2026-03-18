from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    BOT_TOKEN: str = Field(
        ..., min_length=10, description="Bot token from @BotFather or from VK_API"
    )
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"


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
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"

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

    @property
    def app(self) -> AppSettings:
        return AppSettings(
            BOT_TOKEN=self.BOT_TOKEN,
            ENVIRONMENT=self.ENVIRONMENT,
            TIMEZONE=self.TIMEZONE,
        )

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(DATABASE_URL=self.DATABASE_URL)


settings = Settings()  # type:ignore[call-arg]
