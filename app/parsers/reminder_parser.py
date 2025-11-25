from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from datetime import datetime, timedelta
from typing import Optional
import re
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
        4. Конкретная дата: "2024-11-20 19:00"
        """
        if not time or not isinstance(time, str):
            return None
        
        time = time.strip().lower()
        now = datetime.now()
        
        # ============ ФОРМАТ 1: Конкретная дата ============
        try:
            if " " in time and ":" in time:
                return datetime.strptime(time, "%Y-%m-%d %H:%M")
            
            if re.match(r"^\d{4}-\d{2}-\d{2}$", time):
                date_obj = datetime.strptime(time, "%Y-%m-%d")
                return date_obj.replace(hour=9, minute=0)
        except ValueError:
            pass
        
        # ============ ФОРМАТ 2: Время дня (HH:MM) ============
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
        
        # ============ ФОРМАТ 3: Завтра ============
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
        
        # ============ ФОРМАТ 4: Относительное время ============
        if time.startswith("через "):
            time_part = time.replace("через", "").strip()
            
            match = re.match(r"^(\d+)\s*(часа?|часов|минут?|дня?|дней|неделя?|недель)$", time_part)
            
            if match:
                count = int(match.group(1))
                unit = match.group(2)
                
                if unit in ["час", "часа", "часов"]:
                    return now + timedelta(hours=count)
                elif unit in ["минута", "минут"]:
                    return now + timedelta(minutes=count)
                elif unit in ["день", "дня", "дней"]:
                    return now + timedelta(days=count)
                elif unit in ["неделя", "недель"]:
                    return now + timedelta(weeks=count)
        
        return None

    def parseReminderPriority(self, priority: str) -> Optional[str]:
        if not priority or not isinstance(priority, str):
            return None
        
        normalized = priority.strip().lower()
        
        try:
            priority_enum = Priority(normalized)
            return priority_enum.value
        except ValueError:
            return None

    def parseReminderFrequency(self, freq: str):
        if not freq or not isinstance(freq, str):
            return None
        
        normalized = freq.strip().lower()
        
        try:
            freq_enum = RepeatedValue(normalized)
            return freq_enum.value
        except ValueError:
            return None


    def parse(self, reminderText: str, telegram_id: int):
        # /remind <текст> | <время> [| приоритет] [| повтор]
        reminderParams = reminderText.split("|")
        match (len(reminderParams)):
            case 2:
                desc = self.parseReminderDescription(reminderParams[0])
                time = self.parseReminderTime(reminderParams[1])

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
                priority = self.parseReminderPriority(reminderParams[2])
                if priority is None:
                    frequency = self.parseReminderFrequency(reminderParams[2])
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
                priority = self.parseReminderPriority(reminderParams[2])
                frequency = self.parseReminderFrequency(reminderParams[3])
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