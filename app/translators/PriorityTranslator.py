from app.translators.TranslatorMixin import FromRuTranslatorMixin

class PriorityTranslator(FromRuTranslatorMixin):
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