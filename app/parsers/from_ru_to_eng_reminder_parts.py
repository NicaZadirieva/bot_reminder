from app.entities.reminder import Priority, RepeatedValue, ReminderStatus

def from_ru_to_eng_reminder_priority(priority: str):
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

def from_ru_to_eng_reminder_freq(freq: str):
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