import pytest


# ============ ИМПОРТЫ ============
from app.parsers.reminder_priority_parser import ReminderPriorityParser
from app.entities.reminder import Priority

# ============ ТЕСТЫ parseReminderPriority ============

class TestParseReminderPriority:
    """Тесты для parseReminderPriority"""
    
    # ✅ ВАЛИДНЫЕ ПРИОРИТЕТЫ
    def test_parse_priority_high(self):
        """'high'"""
        assert ReminderPriorityParser.parseReminderPriority("high") == Priority.HIGH
    
    def test_parse_priority_medium(self):
        """'medium'"""
        assert ReminderPriorityParser.parseReminderPriority("medium") == Priority.MEDIUM
    
    def test_parse_priority_low(self):
        """'low'"""
        assert ReminderPriorityParser.parseReminderPriority("low") == Priority.LOW
    
    # ✅ РАЗНЫЕ РЕГИСТРЫ
    def test_parse_priority_uppercase(self):
        """Приоритет в верхнем регистре"""
        assert ReminderPriorityParser.parseReminderPriority("HIGH") == Priority.HIGH
        assert ReminderPriorityParser.parseReminderPriority("MEDIUM") == Priority.MEDIUM
    
    def test_parse_priority_mixed_case(self):
        """Приоритет в смешанном регистре"""
        assert ReminderPriorityParser.parseReminderPriority("High") == Priority.HIGH
        assert ReminderPriorityParser.parseReminderPriority("MeDiUm") == Priority.MEDIUM
    
    # ✅ С ПРОБЕЛАМИ
    def test_parse_priority_with_spaces(self):
        """Приоритет с пробелами"""
        assert ReminderPriorityParser.parseReminderPriority("  high  ") == Priority.HIGH
    
    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_priority_invalid(self):
        """Невалидные значения"""
        assert ReminderPriorityParser.parseReminderPriority("invalid") is None
        assert ReminderPriorityParser.parseReminderPriority("") is None
        assert ReminderPriorityParser.parseReminderPriority(None) is None