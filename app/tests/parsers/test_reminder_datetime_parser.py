import pytest
from datetime import datetime, timedelta


# ============ ИМПОРТЫ ============
from app.parsers.reminder_datetime_parser import ReminderDateTimeParser
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
