from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from datetime import datetime, timedelta
from typing import Optional
import re

from app.parsers.from_ru_to_eng_reminder_parts import from_ru_to_eng_reminder_priority, from_ru_to_eng_reminder_freq
# Parser income data
class ReminderParser:
    def parseReminderDescription(self, description: str):
        return description.strip()

    def parseReminderTime(self, time: str) -> Optional[datetime]:
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
    
        # ============ ФОРМАТ 3: Время дня (HH:MM) ============
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

    def parseReminderPriority(self, priority: str) -> Optional[str]:
        if not priority or not isinstance(priority, str):
            return None
        
        normalized = priority.strip().lower()
        
        try:
            priority_enum = Priority(normalized)
            return priority_enum
        except ValueError:
            return None

    def parseReminderFrequency(self, freq: str):
        if not freq or not isinstance(freq, str):
            return None
        
        normalized = freq.strip().lower()
        
        try:
            freq_enum = RepeatedValue(normalized)
            return freq_enum
        except ValueError:
            return None


    def parse(self, reminderText: str, telegram_id: int):
        # /remind <текст> | <время> [| приоритет] [| повтор]
        reminderParams = reminderText.split("|")
        match (len(reminderParams)):
            case 2:
                desc = self.parseReminderDescription(reminderParams[0])
                if not desc:
                    raise ValueError(f"Invalid desc format: '{reminderParams[0]}'")

                time = self.parseReminderTime(reminderParams[1])

                if not time:
                    raise ValueError(f"Invalid time format: '{reminderParams[1]}'")

                return Reminder(
                    telegram_id=telegram_id,
                    text=desc,
                    remind_at=time,
                    priority=Priority.MEDIUM,
                    status=ReminderStatus.ACTIVE, 
                    repeated_value=RepeatedValue.ONCE
                )
            case 3:
                desc = self.parseReminderDescription(reminderParams[0])
                time = self.parseReminderTime(reminderParams[1])

                priority = self.parseReminderPriority(
                    from_ru_to_eng_reminder_priority(reminderParams[2])
                )

                if not desc:
                    raise ValueError(f"Invalid desc format: '{reminderParams[0]}'")

                if not time:
                    raise ValueError(f"Invalid time format: '{reminderParams[1]}'")

                if priority is None:

                    frequency = self.parseReminderFrequency(
                            from_ru_to_eng_reminder_freq(reminderParams[2])
                    )
       
                    if not frequency:
                        raise ValueError(f"Invalid frequency: '{reminderParams[2]}'")
                    return Reminder(
                        telegram_id=telegram_id,
                        text=desc,
                        remind_at=time,
                        priority=Priority.MEDIUM,
                        status=ReminderStatus.ACTIVE, 
                        repeated_value=frequency
                    )
                else:
                    return Reminder(
                        telegram_id=telegram_id,
                        text=desc,
                        remind_at=time,
                        priority=priority,
                        status=ReminderStatus.ACTIVE, 
                        repeated_value=RepeatedValue.ONCE
                    )
            case 4:
                desc = self.parseReminderDescription(reminderParams[0])
                time = self.parseReminderTime(reminderParams[1])

                priority =  self.parseReminderPriority(
                    from_ru_to_eng_reminder_priority(reminderParams[2])
                )
                frequency = self.parseReminderFrequency(
                    from_ru_to_eng_reminder_freq(reminderParams[3])
                )

                if not desc:
                    raise ValueError(f"Invalid desc format: '{reminderParams[0]}'")
                if not time:
                    raise ValueError(f"Invalid time format: '{reminderParams[1]}'")
                if not priority:
                    raise ValueError(f"Invalid priority: '{reminderParams[2]}'")
                if not frequency:
                    raise ValueError(f"Invalid frequency: '{reminderParams[3]}'")

                return Reminder(
                        telegram_id=telegram_id,
                        text=desc,
                        remind_at=time,
                        priority=priority,
                        status=ReminderStatus.ACTIVE, 
                        repeated_value=frequency
                    )
            case _:
                raise ValueError("Invalid format of reminder text")