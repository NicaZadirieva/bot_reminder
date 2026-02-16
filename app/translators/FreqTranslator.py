from app.translators.TranslatorMixin import FromRuTranslatorMixin, FromEngTranslatorMixin
from app.entities.reminder import RepeatedValue

class FreqTranslator(FromRuTranslatorMixin, FromEngTranslatorMixin):
    @staticmethod
    def from_ru_to_eng(freq: str):
        """
            Переводит русское написание частотности напоминания в английский вариант
        
            Поддерживаемые форматы:
            1. ежедневно
            2. еженедельно
            3. ежемесячно
            4. ежегодно
            5. разово
        """
        freqLowered = freq.lower().strip()
        if freqLowered == "ежедневно":
            return "daily"
        elif freqLowered == "еженедельно":
            return "weekly"
        elif freqLowered == "ежемесячно":
            return "monthly"
        elif freqLowered == "ежегодно":
            return "yearly"
        elif freqLowered == "разово":
            return "once"
        return freq

    @staticmethod
    def eng_to_ru(repeated_value: RepeatedValue):
        repeated_value_str = repeated_value.value
        if repeated_value_str == "daily":
            return "ЕЖЕДНЕВНО"
        elif repeated_value_str == "monthly":
            return "ЕЖЕМЕСЯЧНО"
        elif repeated_value_str == "weekly":
            return "ЕЖЕНЕДЕЛЬНО"
        elif repeated_value_str == "yearly":
            return "ЕЖЕГОДНО"
        elif repeated_value_str == "once":
            return "РАЗОВО"
        else:
            # default
            return "РАЗОВО"
