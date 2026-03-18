from datetime import datetime, timezone as dt_timezone
from pytz import timezone

from app.core import settings


class TimeUtils:
    @staticmethod
    def get_tz() -> timezone:
        # TODO: удалить get_tz
        return timezone(settings.app.TIMEZONE)

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
