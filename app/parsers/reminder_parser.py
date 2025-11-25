from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from typing import Optional
# Parser income data
class ReminderParser:
    def parseReminderDescription(self, description: str):
        return description.strip()

    def parseReminderTime(self, time: str):
        pass

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