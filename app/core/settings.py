from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonAppSettings(BaseModel):
    ENVIRONMENT: str = "development"
    TIMEZONE: str = "Europe/Moscow"


class TgAppSettings(BaseModel):
    TG_BOT_TOKEN: Optional[str] = None
    TG_RUN: bool = False


class VkAppSettings(BaseModel):
    VK_API_TOKEN: Optional[str] = None
    VK_GROUP_ID: Optional[str] = None
    VK_RUN: bool = False


class DatabaseSettings(BaseModel):
    DATABASE_URL: str = Field(..., min_length=10, description="Database connection URL")
    DATABASE_URL_SYNC: str = Field(
        ..., min_length=10, description="Database connection sync URL"
    )

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
    # Telegram
    TG_BOT_TOKEN: Optional[str] = None
    TG_RUN: bool = False
    # VK
    VK_API_TOKEN: Optional[str] = None
    VK_GROUP_ID: Optional[str] = None
    VK_RUN: bool = False
    # Database
    DATABASE_URL: str = Field(..., min_length=10)
    DATABASE_URL_SYNC: str = Field(..., min_length=10)

    # Common
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

    @model_validator(mode="after")
    def validate_correct_running(self):
        if self.VK_RUN and self.TG_RUN:
            raise ValueError("Cannot run several bots on one server:port")
        if self.VK_RUN:
            if not self.VK_API_TOKEN or not self.VK_GROUP_ID:
                raise ValueError("VK_API_TOKEN and VK_GROUP_ID must be provided")
            if not self.VK_GROUP_ID.isdigit():
                raise ValueError("VK_GROUP_ID must be correct number")
        if self.TG_RUN:
            if not self.TG_BOT_TOKEN:
                raise ValueError("TG_BOT_TOKEN must be provided")
        return self

    @property
    def common_app(self) -> CommonAppSettings:
        return CommonAppSettings(
            ENVIRONMENT=self.ENVIRONMENT,
            TIMEZONE=self.TIMEZONE,
        )

    @property
    def tg_app(self) -> TgAppSettings:
        return TgAppSettings(TG_BOT_TOKEN=self.TG_BOT_TOKEN, TG_RUN=self.TG_RUN)

    @property
    def vk_app(self) -> VkAppSettings:
        return VkAppSettings(
            VK_API_TOKEN=self.VK_API_TOKEN,
            VK_GROUP_ID=self.VK_GROUP_ID,
            VK_RUN=self.VK_RUN,
        )

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(
            DATABASE_URL=self.DATABASE_URL, DATABASE_URL_SYNC=self.DATABASE_URL_SYNC
        )


settings = Settings()  # type:ignore[call-arg]
