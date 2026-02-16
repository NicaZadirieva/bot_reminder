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
from app.parsers.reminder_parser import ReminderParser
from app.entities.reminder import Reminder, Priority, RepeatedValue, ReminderStatus
from app.parsers.reminder_datetime_parser import ReminderDateTimeParser

# ============ ТЕСТЫ parseReminderDescription ============

class TestParseReminderDescription:
    """Тесты для parseReminderDescription"""
    
    @pytest.fixture
    def parser(self):
        return ReminderDescParser()
    
    # ✅ ВАЛИДНЫЕ ВХОДЫ
    def test_parse_description_simple(self, parser):
        """Простое описание"""
        result = parser.parseReminderDescription("Buy milk")
        assert result == "Buy milk"
    
    def test_parse_description_with_spaces(self, parser):
        """Описание с пробелами"""
        result = parser.parseReminderDescription("  Buy milk  ")
        assert result == "Buy milk"
    
    def test_parse_description_cyrillic(self, parser):
        """Описание на русском"""
        result = parser.parseReminderDescription("  Купить молоко  ")
        assert result == "Купить молоко"
    
    # ❌ ГРАНИЧНЫЕ СЛУЧАИ
    def test_parse_description_empty(self, parser):
        """Пустая строка"""
        result = parser.parseReminderDescription("")
        assert result == ""


# ============ ТЕСТЫ parseReminderTime ============

class TestParseReminderTime:
    """Тесты для parseReminderTime"""
    
    @pytest.fixture
    def parser(self):
        return ReminderDateTimeParser()
    
    # ✅ ВРЕМЯ ДНЕЙ (HH:MM)
    def test_parse_time_today(self, parser):
        """Время: 18:00"""
        result = parser.parseReminderTime("18:00")
        assert result is not None
        assert result.hour == 18
        assert result.minute == 0
    
    def test_parse_time_with_minutes(self, parser):
        """Время с минутами: 14:30"""
        result = parser.parseReminderTime("14:30")
        assert result is not None
        assert result.hour == 14
        assert result.minute == 30
    
    # ✅ ЗАВТРА
    def test_parse_tomorrow(self, parser):
        """'завтра'"""
        result = parser.parseReminderTime("завтра")
        assert result is not None
        assert result.hour == 9
        
        tomorrow = datetime.now() + timedelta(days=1)
        assert result.day == tomorrow.day
    
    def test_parse_tomorrow_with_time(self, parser):
        """'завтра 15:30'"""
        result = parser.parseReminderTime("завтра 15:30")
        assert result is not None
        assert result.hour == 15
        assert result.minute == 30
    
    # ✅ ОТНОСИТЕЛЬНОЕ ВРЕМЯ
    def test_parse_relative_hours(self, parser):
        """'через 2 часа'"""
        result = parser.parseReminderTime("через 2 часа")
        assert result is not None
        
        now = datetime.now()
        diff = (result - now).total_seconds()
        assert 7190 < diff < 7210  # ~2 часа
    
    def test_parse_relative_minutes(self, parser):
        """'через 30 минут'"""
        result = parser.parseReminderTime("через 30 минут")
        assert result is not None
        
        now = datetime.now()
        diff = (result - now).total_seconds()
        assert 1790 < diff < 1810  # ~30 минут
    
    def test_parse_relative_days(self, parser):
        """'через 1 день'"""
        result = parser.parseReminderTime("через 1 день")
        assert result is not None
        
        expected = datetime.now() + timedelta(days=1)
        assert result.day == expected.day
    
    # ✅ КОНКРЕТНАЯ ДАТА
    def test_parse_date_with_time(self, parser):
        """'2024-11-20 19:00'"""
        result = parser.parseReminderTime("2024-11-20 19:00")
        assert result is not None
        assert result.year == 2024
        assert result.month == 11
        assert result.day == 20
        assert result.hour == 19
        assert result.minute == 0
    
    def test_parse_date_only(self, parser):
        """'2024-11-20'"""
        result = parser.parseReminderTime("2024-11-20")
        assert result is not None
        assert result.year == 2024
        assert result.hour == 9  # Дефолт
    
    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_time_invalid(self, parser):
        """Неправильный формат"""
        assert parser.parseReminderTime("invalid") is None
        assert parser.parseReminderTime("25:00") is None
        assert parser.parseReminderTime("") is None
        assert parser.parseReminderTime(None) is None


# ============ ТЕСТЫ parseReminderPriority ============

class TestParseReminderPriority:
    """Тесты для parseReminderPriority"""
    
    @pytest.fixture
    def parser(self):
        return ReminderParser()
    
    # ✅ ВАЛИДНЫЕ ПРИОРИТЕТЫ
    def test_parse_priority_high(self, parser):
        """'high'"""
        assert parser.parseReminderPriority("high") == Priority.HIGH
    
    def test_parse_priority_medium(self, parser):
        """'medium'"""
        assert parser.parseReminderPriority("medium") == Priority.MEDIUM
    
    def test_parse_priority_low(self, parser):
        """'low'"""
        assert parser.parseReminderPriority("low") == Priority.LOW
    
    # ✅ РАЗНЫЕ РЕГИСТРЫ
    def test_parse_priority_uppercase(self, parser):
        """Приоритет в верхнем регистре"""
        assert parser.parseReminderPriority("HIGH") == Priority.HIGH
        assert parser.parseReminderPriority("MEDIUM") == Priority.MEDIUM
    
    def test_parse_priority_mixed_case(self, parser):
        """Приоритет в смешанном регистре"""
        assert parser.parseReminderPriority("High") == Priority.HIGH
        assert parser.parseReminderPriority("MeDiUm") == Priority.MEDIUM
    
    # ✅ С ПРОБЕЛАМИ
    def test_parse_priority_with_spaces(self, parser):
        """Приоритет с пробелами"""
        assert parser.parseReminderPriority("  high  ") == Priority.HIGH
    
    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_priority_invalid(self, parser):
        """Невалидные значения"""
        assert parser.parseReminderPriority("invalid") is None
        assert parser.parseReminderPriority("") is None
        assert parser.parseReminderPriority(None) is None


# ============ ТЕСТЫ parseReminderFrequency ============

class TestParseReminderFrequency:
    """Тесты для parseReminderFrequency"""
    
    @pytest.fixture
    def parser(self):
        return ReminderParser()
    
    # ✅ ВАЛИДНЫЕ ЧАСТОТЫ
    def test_parse_frequency_once(self, parser):
        """'once'"""
        assert parser.parseReminderFrequency("once") == RepeatedValue.ONCE
    
    def test_parse_frequency_daily(self, parser):
        """'daily'"""
        assert parser.parseReminderFrequency("daily") == RepeatedValue.DAILY
    
    def test_parse_frequency_weekly(self, parser):
        """'weekly'"""
        assert parser.parseReminderFrequency("weekly") == RepeatedValue.WEEKLY
    
    # ✅ РАЗНЫЕ РЕГИСТРЫ
    def test_parse_frequency_uppercase(self, parser):
        """Частота в верхнем регистре"""
        assert parser.parseReminderFrequency("DAILY") == RepeatedValue.DAILY
    
    def test_parse_frequency_with_spaces(self, parser):
        """Частота с пробелами"""
        assert parser.parseReminderFrequency("  daily  ") == RepeatedValue.DAILY
    
    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_frequency_invalid(self, parser):
        """Невалидные значения"""
        assert parser.parseReminderFrequency("invalid") is None
        assert parser.parseReminderFrequency("") is None


# ============ ИНТЕГРАЦИОННЫЕ ТЕСТЫ ============

class TestReminderParserIntegration:
    """Интеграционные тесты для полного парсера"""
    
    @pytest.fixture
    def parser(self):
        return ReminderParser()
    
    # ✅ ПРИМЕРЫ ИЗ ЗАДАНИЯ
    def test_parse_example_1(self, parser):
        """Купить молоко | 18:00"""
        reminder_text = "Купить молоко | 18:00"
        result = parser.parse(reminder_text, telegram_id=123456789)
    
        assert result is not None
        assert result.text == "Купить молоко"
        assert result.remind_at.hour == 18
    
        # ✅ ПРАВИЛЬНО: Сравнивать с Enum объектами!
        assert result.priority == Priority.MEDIUM
        assert result.status == ReminderStatus.ACTIVE
        assert result.repeated_value == RepeatedValue.ONCE
    
    def test_parse_example_2(self, parser):
        """Встреча с командой | завтра 15:30"""
        reminder_text = "Встреча с командой | завтра 15:30"
        result = parser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Встреча с командой"
        assert result.remind_at.hour == 15
        assert result.remind_at.minute == 30
    
    def test_parse_example_3(self, parser):
        """Позвонить маме | через 2 часа"""
        reminder_text = "Позвонить маме | через 2 часа"
        result = parser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Позвонить маме"
    
    def test_parse_example_4(self, parser):
        """Рабочая встреча | 09:00 | HIGH | daily"""
        reminder_text = "Рабочая встреча | 09:00 | HIGH | daily"
        result = parser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Рабочая встреча"
        assert result.remind_at.hour == 9
        assert result.priority == Priority.HIGH
        assert result.repeated_value == RepeatedValue.DAILY
    
    def test_parse_example_5(self, parser):
        """Купить подарок | 2024-11-20 19:00 | MEDIUM | once"""
        reminder_text = "Купить подарок | 2024-11-20 19:00 | MEDIUM | once"
        result = parser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Купить подарок"
        assert result.remind_at.year == 2024
        assert result.remind_at.month == 11
        assert result.remind_at.day == 20
        assert result.remind_at.hour == 19
        assert result.priority == Priority.MEDIUM
        assert result.repeated_value == RepeatedValue.ONCE
    
    # ❌ НЕВАЛИДНЫЕ ФОРМАТЫ
    def test_parse_invalid_format(self, parser):
        """Неправильное количество параметров"""
        with pytest.raises(ValueError, match="Invalid format"):
            parser.parse("Only one parameter", telegram_id=123)
    
    def test_parse_with_spaces(self, parser):
        """Пробелы вокруг '|'"""
        reminder_text = "Купить молоко  |  18:00  |  high"
        result = parser.parse(reminder_text, telegram_id=123456789)
        
        assert result is not None
        assert result.text == "Купить молоко"
        assert result.priority == Priority.HIGH
    
    def test_parse_invalid_time_throws_error(self, parser):
        """Невалидное время"""
        reminder_text = "Купить молоко | invalid_time"
    
        # ✅ ПРАВИЛЬНО: Ловить ValueError
        with pytest.raises(ValueError):
            parser.parse(reminder_text, telegram_id=123)