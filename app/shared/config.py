# Configuration

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()


class Config:
    def __init__(self):
        # Telegram
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "default_token")

        # Database
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL", "sqlite+aiosqlite:///./reminder_bot.db"
        )

        # Environment
        self.DEBUG = os.getenv("DEBUG", "False") == "True"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.TIMEZONE = os.getenv("TIMEZONE", "UTC")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


config = Config()
