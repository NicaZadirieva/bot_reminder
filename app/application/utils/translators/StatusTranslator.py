from app.domain.entities import StatusEntity
from app.application.utils.translators.TranslatorMixin import FromEngTranslatorMixin


class StatusTranslator(FromEngTranslatorMixin):
    @staticmethod
    def from_eng_to_ru(status: StatusEntity):
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
