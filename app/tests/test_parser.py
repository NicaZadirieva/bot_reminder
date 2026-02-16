# Parser test
# coding: utf-8
"""
ТЕСТЫ ДЛЯ ReminderParser

Полный набор unit и интеграционных тестов для парсера напоминаний
"""

import pytest
from datetime import datetime, timedelta
from typing import Optional
import re


# ============ ИМПОРТЫ ============

from app.parsers.reminder_desc_parser import ReminderDescParser
from app.parsers.reminder_parser import ReminderFrequencyParser, ReminderParser, ReminderPriorityParser
from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from app.parsers.reminder_datetime_parser import ReminderDateTimeParser

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


# ============ ТЕСТЫ parseReminderTime ============

class TestParseReminderTime:
    """Тесты для parseReminderTime"""
    
    # ✅ ВРЕМЯ ДНЕЙ (HH:MM)
    def test_parse_time_today(self):
        """Время: 18:00"""
        result = ReminderDateTimeParser.parseReminderTime("18:00")
        assert result is not None
        assert result.hour == 18
        assert result.minute == 0
    
    def test_parse_time_with_minutes(self):
        """Время с минутами: 14:30"""
        result = ReminderDateTimeParser.parseReminderTime("14:30")
        assert result is not None
        assert result.hour == 14
        assert result.minute == 30
    
    # ✅ ЗАВТРА
    def test_parse_tomorrow(self):
        """'завтра'"""
        result = ReminderDateTimeParser.parseReminderTime("завтра")
        assert result is not None
        assert result.hour == 9
        
        tomorrow = datetime.now() + timedelta(days=1)
        assert result.day == tomorrow.day
    
    def test_parse_tomorrow_with_time(self):
        """'завтра 15:30'"""
        result = ReminderDateTimeParser.parseReminderTime("завтра 15:30")
        assert result is not None
        assert result.hour == 15
        assert result.minute == 30
    
    # ✅ ОТНОСИТЕЛЬНОЕ ВРЕМЯ
    def test_parse_relative_hours(self):
        """'через 2 часа'"""
        result = ReminderDateTimeParser.parseReminderTime("через 2 часа")
        assert result is not None
        
        now = datetime.now()
        diff = (result - now).total_seconds()
        assert 7190 < diff < 7210  # ~2 часа
    
    def test_parse_relative_minutes(self):
        """'через 30 минут'"""
        result = ReminderDateTimeParser.parseReminderTime("через 30 минут")
        assert result is not None
        
        now = datetime.now()
        diff = (result - now).total_seconds()
        assert 1790 < diff < 1810  # ~30 минут
    
    def test_parse_relative_days(self):
        """'через 1 день'"""
        result = ReminderDateTimeParser.parseReminderTime("через 1 день")
        assert result is not None
        
        expected = datetime.now() + timedelta(days=1)
        assert result.day == expected.day
    
    # ✅ КОНКРЕТНАЯ ДАТА
    def test_parse_date_with_time(self):
        """'2024-11-20 19:00'"""
        result = ReminderDateTimeParser.parseReminderTime("2024-11-20 19:00")
        assert result is not None
        assert result.year == 2024
        assert result.month == 11
        assert result.day == 20
        assert result.hour == 19
        assert result.minute == 0
    
    def test_parse_date_only(self):
        """'2024-11-20'"""
        result = ReminderDateTimeParser.parseReminderTime("2024-11-20")
        assert result is not None
        assert result.year == 2024
        assert result.hour == 9  # Дефолт
    
    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_time_invalid(self):
        """Неправильный формат"""
        assert ReminderDateTimeParser.parseReminderTime("invalid") is None
        assert ReminderDateTimeParser.parseReminderTime("25:00") is None
        assert ReminderDateTimeParser.parseReminderTime("") is None
        assert ReminderDateTimeParser.parseReminderTime(None) is None


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


# ============ ТЕСТЫ parseReminderFrequency ============

class TestParseReminderFrequency:
    """Тесты для parseReminderFrequency"""
    
    # ✅ ВАЛИДНЫЕ ЧАСТОТЫ
    def test_parse_frequency_once(self):
        """'once'"""
        assert ReminderFrequencyParser.parseReminderFrequency("once") == RepeatedValue.ONCE
    
    def test_parse_frequency_daily(self):
        """'daily'"""
        assert ReminderFrequencyParser.parseReminderFrequency("daily") == RepeatedValue.DAILY
    
    def test_parse_frequency_weekly(self):
        """'weekly'"""
        assert ReminderFrequencyParser.parseReminderFrequency("weekly") == RepeatedValue.WEEKLY
    
    # ✅ РАЗНЫЕ РЕГИСТРЫ
    def test_parse_frequency_uppercase(self):
        """Частота в верхнем регистре"""
        assert ReminderFrequencyParser.parseReminderFrequency("DAILY") == RepeatedValue.DAILY
    
    def test_parse_frequency_with_spaces(self):
        """Частота с пробелами"""
        assert ReminderFrequencyParser.parseReminderFrequency("  daily  ") == RepeatedValue.DAILY
    
    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_frequency_invalid(self):
        """Невалидные значения"""
        assert ReminderFrequencyParser.parseReminderFrequency("invalid") is None
        assert ReminderFrequencyParser.parseReminderFrequency("") is None


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