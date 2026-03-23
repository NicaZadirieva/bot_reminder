from typing import Optional
from app.models import Priority


class ReminderPriorityParser:
    @staticmethod
    def parseReminderPriority(priority: str) -> Optional[Priority]:
        if not priority or not isinstance(priority, str):
            return None

        normalized = priority.strip().lower()

        try:
            priority_enum = Priority(normalized)
            return priority_enum
        except ValueError:
            return None

    @staticmethod
    def from_ru_to_eng(priority: str):
        """
        Переводит русское написание приоритетности напоминания в английский вариант

        Поддерживаемые форматы:
        1. высокий
        2. низкий
        3. средний
        """
        priorityLowered = priority.lower().strip()
        if priorityLowered == "высокий":
            return "HIGH"
        elif priorityLowered == "низкий":
            return "LOW"
        elif priorityLowered == "средний":
            return "MEDIUM"
        return priority
