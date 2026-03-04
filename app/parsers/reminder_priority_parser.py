from typing import Optional
from app.entities import PriorityEntity
from app.translators.TranslatorMixin import FromRuTranslatorMixin

class ReminderPriorityParser(FromRuTranslatorMixin):
    @staticmethod
    def parseReminderPriority(priority: str) -> Optional[str]:
        if not priority or not isinstance(priority, str):
            return None
        
        normalized = priority.strip().lower()
        
        try:
            priority_enum = PriorityEntity(normalized)
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