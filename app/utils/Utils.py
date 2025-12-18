# app/utils/Utils.py (или utils.py)
from datetime import datetime, timezone as dt_timezone
from pytz import timezone

class Utils:
    @staticmethod
    def get_tz() -> timezone:
        """Получить timezone Moscow"""
        return timezone('Europe/Moscow')
    
    @staticmethod
    def get_now() -> datetime:
        """Получить текущее время в Moscow timezone"""
        tz = Utils.get_tz()
        now = datetime.now(tz)
        return now
    
    @staticmethod
    def _make_aware(dt: datetime) -> datetime:
        """Конвертировать naive datetime в timezone-aware"""
        tz = Utils.get_tz()
        if dt.tzinfo is None:
            return tz.localize(dt)
        return dt
