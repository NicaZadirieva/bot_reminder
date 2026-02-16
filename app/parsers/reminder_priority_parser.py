from typing import Optional
from app.entities.reminder import Priority

class ReminderPriorityParser():
    def parseReminderPriority(self, priority: str) -> Optional[str]:
        if not priority or not isinstance(priority, str):
            return None
        
        normalized = priority.strip().lower()
        
        try:
            priority_enum = Priority(normalized)
            return priority_enum
        except ValueError:
            return None