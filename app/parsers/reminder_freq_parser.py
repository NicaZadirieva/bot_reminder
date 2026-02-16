from typing import Optional
from app.entities.reminder import RepeatedValue

class ReminderFrequencyParser():
    @staticmethod
    def parseReminderFrequency(freq: str):
        if not freq or not isinstance(freq, str):
            return None
        
        normalized = freq.strip().lower()
        
        try:
            freq_enum = RepeatedValue(normalized)
            return freq_enum
        except ValueError:
            return None
