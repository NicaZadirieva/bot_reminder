import pytest


# ============ ИМПОРТЫ ============

from app.parsers.reminder_desc_parser import ReminderDescParser

# ============ ТЕСТЫ parseReminderDescription ============

class TestParseReminderDescription:
    """Тесты для parseReminderDescription"""
    
    # ✅ ВАЛИДНЫЕ ВХОДЫ
    def test_parse_description_simple(self):
        """Простое описание"""
        result = ReminderDescParser.parseReminderDescription("Buy milk")
        assert result == "Buy milk"
    
    def test_parse_description_with_spaces(self):
        """Описание с пробелами"""
        result = ReminderDescParser.parseReminderDescription("  Buy milk  ")
        assert result == "Buy milk"
    
    def test_parse_description_cyrillic(self):
        """Описание на русском"""
        result = ReminderDescParser.parseReminderDescription("  Купить молоко  ")
        assert result == "Купить молоко"
    
    # ❌ ГРАНИЧНЫЕ СЛУЧАИ
    def test_parse_description_empty(self):
        """Пустая строка"""
        result = ReminderDescParser.parseReminderDescription("")
        assert result == ""

