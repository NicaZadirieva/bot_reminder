from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from datetime import datetime, timedelta
from typing import Optional
import re

from app.parsers.from_ru_to_eng_reminder_parts import from_ru_to_eng_reminder_priority, from_ru_to_eng_reminder_freq
from app.parsers.reminder_datetime_parser import ReminderDateTimeParser
from app.parsers.reminder_desc_parser import ReminderDescParser
from app.parsers.reminder_freq_parser import ReminderFrequencyParser
from app.parsers.reminder_priority_parser import ReminderPriorityParser

# Parser income data
class ReminderParser:
    @staticmethod
    def parse(reminderText: str, telegram_id: int):
        # /remind <текст> | <время> [| приоритет] [| повтор]
        reminderParams = reminderText.split("|")
        match (len(reminderParams)):
            case 2:
                desc = ReminderDescParser.parseReminderDescription(reminderParams[0])
                if not desc:
                    raise ValueError(f"Invalid desc format: '{reminderParams[0]}'")

                time = ReminderDateTimeParser.parseReminderTime(reminderParams[1])

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
                desc = ReminderDescParser.parseReminderDescription(reminderParams[0])
                time = ReminderDateTimeParser.parseReminderTime(reminderParams[1])

                priority = ReminderPriorityParser.parseReminderPriority(
                    from_ru_to_eng_reminder_priority(reminderParams[2])
                )

                if not desc:
                    raise ValueError(f"Invalid desc format: '{reminderParams[0]}'")

                if not time:
                    raise ValueError(f"Invalid time format: '{reminderParams[1]}'")

                if priority is None:

                    frequency = ReminderFrequencyParser.parseReminderFrequency(
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
                desc = ReminderDescParser.parseReminderDescription(reminderParams[0])
                time = ReminderDateTimeParser.parseReminderTime(reminderParams[1])

                priority =  ReminderPriorityParser.parseReminderPriority(
                    from_ru_to_eng_reminder_priority(reminderParams[2])
                )
                frequency = ReminderFrequencyParser.parseReminderFrequency(
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