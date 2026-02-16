# Parser test
# coding: utf-8
"""
ТЕСТЫ ДЛЯ ReminderParser

Полный набор unit и интеграционных тестов для парсера напоминаний
"""

from app.entities.reminder import Priority, ReminderStatus, RepeatedValue
from app.parsers.reminder_parser import ReminderParser
import pytest

# ============ ИНТЕГРАЦИОННЫЕ ТЕСТЫ ============

class TestReminderParserIntegration:
    """Интеграционные тесты для полного парсера"""
    
    # ✅ ПРИМЕРЫ ИЗ ЗАДАНИЯ
    def test_parse_example_1(self):
        """Купить молоко | 18:00"""
        reminder_text = "Купить молоко | 18:00"
        result = ReminderParser.parse(reminder_text, telegram_id=123456789)
    
        assert result is not None
        assert result.text == "Купить молоко"
        assert result.remind_at.hour == 18
    
        # ✅ ПРАВИЛЬНО: Сравнивать с Enum объектами!
        assert result.priority == Priority.MEDIUM
        assert result.status == ReminderStatus.ACTIVE
        assert result.repeated_value == RepeatedValue.ONCE
    
    def test_parse_example_2(self):
        """Встреча с командой | завтра 15:30"""
        reminder_text = "Встреча с командой | завтра 15:30"
        result = ReminderParser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Встреча с командой"
        assert result.remind_at.hour == 15
        assert result.remind_at.minute == 30
    
    def test_parse_example_3(self):
        """Позвонить маме | через 2 часа"""
        reminder_text = "Позвонить маме | через 2 часа"
        result = ReminderParser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Позвонить маме"
    
    def test_parse_example_4(self):
        """Рабочая встреча | 09:00 | HIGH | daily"""
        reminder_text = "Рабочая встреча | 09:00 | HIGH | daily"
        result = ReminderParser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Рабочая встреча"
        assert result.remind_at.hour == 9
        assert result.priority == Priority.HIGH
        assert result.repeated_value == RepeatedValue.DAILY
    
    def test_parse_example_5(self):
        """Купить подарок | 2024-11-20 19:00 | MEDIUM | once"""
        reminder_text = "Купить подарок | 2024-11-20 19:00 | MEDIUM | once"
        result = ReminderParser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Купить подарок"
        assert result.remind_at.year == 2024
        assert result.remind_at.month == 11
        assert result.remind_at.day == 20
        assert result.remind_at.hour == 19
        assert result.priority == Priority.MEDIUM
        assert result.repeated_value == RepeatedValue.ONCE
    
    # ❌ НЕВАЛИДНЫЕ ФОРМАТЫ
    def test_parse_invalid_format(self):
        """Неправильное количество параметров"""
        with pytest.raises(ValueError, match="Invalid format"):
            ReminderParser.parse("Only one parameter", telegram_id=123)
    
    def test_parse_with_spaces(self):
        """Пробелы вокруг '|'"""
        reminder_text = "Купить молоко  |  18:00  |  high"
        result = ReminderParser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Купить молоко"
        assert result.priority == Priority.HIGH
    
    def test_parse_invalid_time_throws_error(self):
        """Невалидное время"""
        reminder_text = "Купить молоко | invalid_time"
    
        # ✅ ПРАВИЛЬНО: Ловить ValueError
        with pytest.raises(ValueError):
            ReminderParser.parse(reminder_text, telegram_id=123)