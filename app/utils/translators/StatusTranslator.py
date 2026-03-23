from app.models import Status


class StatusTranslator:
    @staticmethod
    def from_eng_to_ru(status: Status):
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
