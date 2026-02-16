from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from datetime import datetime, timedelta
from typing import Optional
import re

from app.parsers.from_ru_to_eng_reminder_parts import from_ru_to_eng_reminder_priority, from_ru_to_eng_reminder_freq
from app.parsers.reminder_datetime_parser import ReminderDateTimeParser

# Parser income data
class ReminderParser:
    def __init__(self):
        self._reminderDateTimeParser = ReminderDateTimeParser()

    def parseReminderDescription(self, description: str):
        return description.strip()

    

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

                time = self._reminderDateTimeParser.parseReminderTime(reminderParams[1])

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
                time = self._reminderDateTimeParser.parseReminderTime(reminderParams[1])

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
                time = self._reminderDateTimeParser.parseReminderTime(reminderParams[1])

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