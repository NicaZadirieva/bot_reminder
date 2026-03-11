import pytest


# ============ ИМПОРТЫ ============
from app.application.utils.parsers.reminder_priority_parser import (
    ReminderPriorityParser,
)
from app.application.domain.entities import PriorityEntity

# ============ ТЕСТЫ parseReminderPriority ============


class TestParseReminderPriority:
    """Тесты для parseReminderPriority"""

    # ✅ ВАЛИДНЫЕ ПРИОРИТЕТЫ
    def test_parse_priority_high(self):
        """'high'"""
        assert (
            ReminderPriorityParser.parseReminderPriority("high") == PriorityEntity.HIGH
        )

    def test_parse_priority_medium(self):
        """'medium'"""
        assert (
            ReminderPriorityParser.parseReminderPriority("medium")
            == PriorityEntity.MEDIUM
        )

    def test_parse_priority_low(self):
        """'low'"""
        assert ReminderPriorityParser.parseReminderPriority("low") == PriorityEntity.LOW

    # ✅ РАЗНЫЕ РЕГИСТРЫ
    def test_parse_priority_uppercase(self):
        """Приоритет в верхнем регистре"""
        assert (
            ReminderPriorityParser.parseReminderPriority("HIGH") == PriorityEntity.HIGH
        )
        assert (
            ReminderPriorityParser.parseReminderPriority("MEDIUM")
            == PriorityEntity.MEDIUM
        )

    def test_parse_priority_mixed_case(self):
        """Приоритет в смешанном регистре"""
        assert (
            ReminderPriorityParser.parseReminderPriority("High") == PriorityEntity.HIGH
        )
        assert (
            ReminderPriorityParser.parseReminderPriority("MeDiUm")
            == PriorityEntity.MEDIUM
        )

    # ✅ С ПРОБЕЛАМИ
    def test_parse_priority_with_spaces(self):
        """Приоритет с пробелами"""
        assert (
            ReminderPriorityParser.parseReminderPriority("  high  ")
            == PriorityEntity.HIGH
        )

    # ❌ НЕВАЛИДНЫЕ ВХОДЫ
    def test_parse_priority_invalid(self):
        """Невалидные значения"""
        assert ReminderPriorityParser.parseReminderPriority("invalid") is None
        assert ReminderPriorityParser.parseReminderPriority("") is None
        assert ReminderPriorityParser.parseReminderPriority(None) is None
