from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from datetime import datetime, timedelta
from typing import Optional
import re


class ReminderDateTimeParser:
    @staticmethod
    def parseFmtDateTime(time: str, now: datetime) -> Optional[datetime]:
        # ============ ФОРМАТ 1: Конкретная дата с временем ============
        # Проверяем форматы с датой и временем
        if " " in time and ":" in time:
            date_part, time_part = time.split(" ", 1)
        
            # Пробуем разные форматы даты
            date_formats = [
                "%Y-%m-%d",  # 2024-11-20
                "%d.%m.%Y",  # 20.11.2024
                "%d/%m/%Y",  # 20/11/2024
                "%d-%m-%Y",  # 20-11-2024
            ]
        
            for date_fmt in date_formats:
                try:
                    # Парсим дату
                    date_obj = datetime.strptime(date_part, date_fmt)
                
                    # Парсим время (поддерживаем HH:MM и HH:MM:SS)
                    if re.match(r"^\d{1,2}:\d{2}(:\d{2})?$", time_part):
                        time_parts = time_part.split(":")
                        hour = int(time_parts[0])
                        minute = int(time_parts[1])
                    
                        # Проверяем корректность времени
                        if not (0 <= hour <= 23 and 0 <= minute <= 59):
                            continue
                    
                        # Устанавливаем время
                        result = date_obj.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                        # Если время уже прошло сегодня и дата сегодняшняя - оставляем как есть
                        # (пользователь указал конкретную дату, даже если она в прошлом)
                        return result
                    
                except (ValueError, IndexError):
                    continue
        return None

    @staticmethod
    def parseOnlyDateFmt(time: str) -> Optional[datetime]:
         # ============ ФОРМАТ 2: Только дата (без времени) ============
        # Проверяем форматы только даты
        date_only_formats = [
            "%Y-%m-%d",   # 2024-11-20
            "%d.%m.%Y",   # 20.11.2024
            "%d/%m/%Y",   # 20/11/2024
            "%d-%m-%Y",   # 20-11-2024
        ]
    
        for date_fmt in date_only_formats:
            try:
                date_obj = datetime.strptime(time, date_fmt)
                # Устанавливаем время по умолчанию - 9:00
                return date_obj.replace(hour=9, minute=0, second=0, microsecond=0)
            except ValueError:
                continue
        return None

    @staticmethod
    def parseOnlyTimeFmt(time: str, now: datetime) -> Optional[datetime]:
        if re.match(r"^\d{1,2}:\d{2}$", time):
            try:
                hour, minute = map(int, time.split(":"))
            
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    return None
            
                reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
                # Если время уже прошло - назначить на завтра
                if reminder_time < now:
                    reminder_time += timedelta(days=1)
            
                return reminder_time
            except (ValueError, IndexError):
                return None
        return None

    @staticmethod
    def parseOnlyTomorrow(time: str, now: datetime) -> Optional[datetime]:
        # ============ ФОРМАТ 4: Завтра ============
        if time.startswith("завтра"):
            tomorrow = now + timedelta(days=1)
        
            if time == "завтра":
                return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        
            time_part = time.replace("завтра", "").strip()
            if re.match(r"^\d{1,2}:\d{2}$", time_part):
                try:
                    hour, minute = map(int, time_part.split(":"))
                    if 0 <= hour <= 23 and 0 <= minute <= 59:
                        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
                except (ValueError, IndexError):
                    return None
        return None

    @staticmethod
    def parseRelativeDateTime(time: str, now: datetime) -> Optional[datetime]:
        # ============ ФОРМАТ 5: Относительное время ============
        if time.startswith("через "):
            time_part = time.replace("через", "").strip()

            match = re.match(r"^(\d+)\s*(часа|часов|час|минута|минуты|минут|день|дня|дней|неделя|недели|недель)$", time_part)

            if match:
                count = int(match.group(1))
                unit = match.group(2)
    
                if unit in ["час", "часа", "часов"]:
                    return now + timedelta(hours=count)
                elif unit in ["минута", "минуты", "минут"]:
                    return now + timedelta(minutes=count)
                elif unit in ["день", "дня", "дней"]:
                    return now + timedelta(days=count)
                elif unit in ["неделя", "недели", "недель"]:
                    return now + timedelta(weeks=count)
        return None
    
    
    @staticmethod
    def parseReminderTime(time: str) -> Optional[datetime]:
        """
        Парсит время напоминания и возвращает объект datetime.
    
        Поддерживаемые форматы:
        1. Время дня: "18:00", "15:30"
        2. Завтра: "завтра", "завтра 15:30"
        3. Относительное: "через 2 часа", "через 30 минут"
        4. Конкретная дата: "2024-11-20 19:00" или "20.11.2024 19:00"
        5. Только дата: "2024-11-20" или "20.11.2024"
        """
        if not time or not isinstance(time, str):
            return None
    
        time = time.strip().lower()
        now = datetime.now()
    
        # ============ ФОРМАТ 1: Конкретная дата с временем ============
        # Проверяем форматы с датой и временем
        fmtDatetime = ReminderDateTimeParser.parseFmtDateTime(time, now)
        if fmtDatetime is not None:
            return fmtDatetime
    
        # ============ ФОРМАТ 2: Только дата (без времени) ============
        # Проверяем форматы только даты
        onlyDateFmt = ReminderDateTimeParser.parseOnlyDateFmt(time)
        if onlyDateFmt is not None:
            return onlyDateFmt
    
        # ============ ФОРМАТ 3: Время дня (HH:MM) ============
        onlyTimeFmt = ReminderDateTimeParser.parseOnlyTimeFmt(time, now)
        if onlyTimeFmt is not None:
            return onlyTimeFmt

        # ============ ФОРМАТ 4: Завтра ============
        onlyTomorrow = ReminderDateTimeParser.parseOnlyTomorrow(time, now)
        if onlyTomorrow is not None:
            return onlyTomorrow
    
        # ============ ФОРМАТ 5: Относительное время ============
        relativeDateTime = ReminderDateTimeParser.parseRelativeDateTime(time, now)
        if relativeDateTime is not None:
            return relativeDateTime

        return None