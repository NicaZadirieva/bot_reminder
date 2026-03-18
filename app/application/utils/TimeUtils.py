from datetime import datetime, timezone as dt_timezone
from pytz import timezone

from app.core import settings


class TimeUtils:
    @staticmethod
    def get_now() -> datetime:
        """Получить текущее время"""
        tz = timezone(settings.app.TIMEZONE)
        now = datetime.now(tz)
        return now

    @staticmethod
    def _make_aware(dt: datetime) -> datetime:
        # TODO: подумать как переименовать
        """Конвертировать naive datetime в timezone-aware"""
        tz = timezone(settings.app.TIMEZONE)
        if dt.tzinfo is None:
            return tz.localize(dt)
        return dt
