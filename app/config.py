# Configuration

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

class Config:
    def __init__(self):
        # Telegram
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', 'default_token')
        self.ADMIN_IDS = os.getenv('ADMIN_IDS', '')
    
        # Database
        self.DATABASE_URL = os.getenv(
            'DATABASE_URL',
            'sqlite+aiosqlite:///./reminder_bot.db'
        )
    
        # Environment
        self.DEBUG = os.getenv('DEBUG', 'False') == 'True'
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
        self.TIMEZONE = os.getenv('TIMEZONE', 'UTC')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.SCHEDULER_CHECK_INTERVAL = int(os.getenv('SCHEDULER_CHECK_INTERVAL', '30'))
        self.MAX_REMINDER_TEXT_LENGTH = int(os.getenv('MAX_REMINDER_TEXT_LENGTH', '200'))

config = Config()