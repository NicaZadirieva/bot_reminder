from datetime import datetime, timedelta, timezone as dt_timezone
from pytz import timezone
class Utils:
     @staticmethod 
     def _make_aware(dt: datetime) -> datetime:
        """🔧 Конвертировать naive datetime в timezone-aware"""
        tz = Utils.get_tz()
        if dt.tzinfo is None:
            # Если datetime naive, добавить timezone Moscow
            return tz.localize(dt)
        return dt
     
     @staticmethod
     def get_now() -> datetime:
         tz = Utils.get_tz()
         now = datetime.now(tz)
         return now

     @staticmethod
     def get_tz() -> timezone:
         return timezone('Europe/Moscow')