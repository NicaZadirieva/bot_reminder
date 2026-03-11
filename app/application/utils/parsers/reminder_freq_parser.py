from app.application.domain.entities import RepeatedValueEntity


class ReminderFrequencyParser:
    @staticmethod
    def parseReminderFrequency(freq: str):
        if not freq or not isinstance(freq, str):
            return None

        normalized = freq.strip().lower()

        try:
            freq_enum = RepeatedValueEntity(normalized)
            return freq_enum
        except ValueError:
            return None
