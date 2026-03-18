from datetime import datetime, timezone as dt_timezone
from pytz import timezone

from app.shared.config import config


class TimeUtils:
    @staticmethod
    def get_tz() -> timezone:
        """Получить timezone Moscow"""
        return timezone(config.TIMEZONE)

    @staticmethod
    def get_now() -> datetime:
        """Получить текущее время в Moscow timezone"""
        tz = TimeUtils.get_tz()
        now = datetime.now(tz)
        return now

    @staticmethod
    def _make_aware(dt: datetime) -> datetime:
        """Конвертировать naive datetime в timezone-aware"""
        tz = TimeUtils.get_tz()
        if dt.tzinfo is None:
            return tz.localize(dt)
        return dt
