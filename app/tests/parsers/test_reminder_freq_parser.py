import pytest

from app.utils.parsers.reminder_freq_parser import ReminderFrequencyParser
from app.entities import RepeatedValueEntity
# ============ ТЕСТЫ parseReminderFrequency ============


class TestParseReminderFrequency:
    """Тесты для parseReminderFrequency"""

    # ✅ ВАЛИДНЫЕ ЧАСТОТЫ
    def test_parse_frequency_once(self):
        """'once'"""
        assert (
            ReminderFrequencyParser.parseReminderFrequency("once")
            == RepeatedValueEntity.ONCE
        )

    def test_parse_frequency_daily(self):
        """'daily'"""
        assert (
            ReminderFrequencyParser.parseReminderFrequency("daily")
            == RepeatedValueEntity.DAILY
        )

    def test_parse_frequency_weekly(self):
        """'weekly'"""
        assert (
            ReminderFrequencyParser.parseReminderFrequency("weekly")
            == RepeatedValueEntity.WEEKLY
        )

    # ✅ РАЗНЫЕ РЕГИСТРЫ
    def test_parse_frequency_uppercase(self):
        """Частота в верхнем регистре"""
        assert (
            ReminderFrequencyParser.parseReminderFrequency("DAILY")
            == RepeatedValueEntity.DAILY
        )

    def test_parse_frequency_with_spaces(self):
        """Частота с пробелами"""
        assert (
            ReminderFrequencyParser.parseReminderFrequency("  daily  ")
            == RepeatedValueEntity.DAILY
        )

    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_frequency_invalid(self):
        """Невалидные значения"""
        assert ReminderFrequencyParser.parseReminderFrequency("invalid") is None
        assert ReminderFrequencyParser.parseReminderFrequency("") is None
