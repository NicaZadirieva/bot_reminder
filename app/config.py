# Configuration

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'default_token')
    ADMIN_IDS = os.getenv('ADMIN_IDS', '')
    
    # Database
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'sqlite+aiosqlite:///./reminder_bot.db'
    )
    
    # Environment
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    SCHEDULER_CHECK_INTERVAL = int(os.getenv('SCHEDULER_CHECK_INTERVAL', '30'))
    MAX_REMINDER_TEXT_LENGTH = int(os.getenv('MAX_REMINDER_TEXT_LENGTH', '200'))

config = Config()