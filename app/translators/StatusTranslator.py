from typing import Optional, List, Any
from app.entities.reminder import ReminderStatus
from app.translators.TranslatorMixin import FromEngTranslatorMixin

class StatusTranslator(FromEngTranslatorMixin):
    @staticmethod
    def from_eng_to_ru(status: ReminderStatus):
        status_str = status.value
        if status_str == "active":
            return "АКТИВНЫЙ"
        elif status_str == "cancelled":
            return "ОТМЕНЕННЫЙ"
        elif status_str == "completed":
            return "ЗАВЕРШЕННЫЙ"
        else:
            # default
            return "АКТИВНЫЙ"