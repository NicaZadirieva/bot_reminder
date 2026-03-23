# Parser test
# coding: utf-8
"""
ТЕСТЫ ДЛЯ ReminderParser

Полный набор unit и интеграционных тестов для парсера напоминаний
"""

from app.domain import Priority, Status, RepeatedValue, Platform
from app.utils.parsers import ReminderParser
import pytest

# ============ ИНТЕГРАЦИОННЫЕ ТЕСТЫ ============


@pytest.fixture
def sample_reminder_parser():
    return ReminderParser(
        platform=Platform.VK,
    )


class TestReminderParserIntegration:
    """Интеграционные тесты для полного парсера"""

    # ✅ ПРИМЕРЫ ИЗ ЗАДАНИЯ
    def test_parse_example_1(self, sample_reminder_parser):
        """Купить молоко | 18:00"""
        reminder_text = "Купить молоко | 18:00"
        result = sample_reminder_parser.parse(reminder_text, user_id=123456789)

        assert result is not None
        assert result.text == "Купить молоко"
        assert result.remind_at.hour == 18

        # ✅ ПРАВИЛЬНО: Сравнивать с Enum объектами!
        assert result.priority == Priority.MEDIUM
        assert result.status == Status.ACTIVE
        assert result.repeated_value == RepeatedValue.ONCE

    def test_parse_example_2(self, sample_reminder_parser):
        """Встреча с командой | завтра 15:30"""
        reminder_text = "Встреча с командой | завтра 15:30"
        result = sample_reminder_parser.parse(reminder_text, user_id=123456789)

        assert result is not None
        assert result.text == "Встреча с командой"
        assert result.remind_at.hour == 15
        assert result.remind_at.minute == 30

    def test_parse_example_3(self, sample_reminder_parser):
        """Позвонить маме | через 2 часа"""
        reminder_text = "Позвонить маме | через 2 часа"
        result = sample_reminder_parser.parse(reminder_text, user_id=123456789)

        assert result is not None
        assert result.text == "Позвонить маме"

    def test_parse_example_4(self, sample_reminder_parser):
        """Рабочая встреча | 09:00 | HIGH | daily"""
        reminder_text = "Рабочая встреча | 09:00 | HIGH | daily"
        result = sample_reminder_parser.parse(reminder_text, user_id=123456789)

        assert result is not None
        assert result.text == "Рабочая встреча"
        assert result.remind_at.hour == 9
        assert result.priority == Priority.HIGH
        assert result.repeated_value == RepeatedValue.DAILY

    def test_parse_example_5(self, sample_reminder_parser):
        """Купить подарок | 2024-11-20 19:00 | MEDIUM | once"""
        reminder_text = "Купить подарок | 2024-11-20 19:00 | MEDIUM | once"
        result = sample_reminder_parser.parse(reminder_text, user_id=123456789)

        assert result is not None
        assert result.text == "Купить подарок"
        assert result.remind_at.year == 2024
        assert result.remind_at.month == 11
        assert result.remind_at.day == 20
        assert result.remind_at.hour == 19
        assert result.priority == Priority.MEDIUM
        assert result.repeated_value == RepeatedValue.ONCE

    # ❌ НЕВАЛИДНЫЕ ФОРМАТЫ
    def test_parse_invalid_format(self, sample_reminder_parser):
        """Неправильное количество параметров"""
        with pytest.raises(ValueError, match="Invalid format"):
            sample_reminder_parser.parse("Only one parameter", user_id=123)

    def test_parse_with_spaces(self, sample_reminder_parser):
        """Пробелы вокруг '|'"""
        reminder_text = "Купить молоко  |  18:00  |  high"
        result = sample_reminder_parser.parse(reminder_text, user_id=123456789)

        assert result is not None
        assert result.text == "Купить молоко"
        assert result.priority == Priority.HIGH

    def test_parse_invalid_time_throws_error(self, sample_reminder_parser):
        """Невалидное время"""
        reminder_text = "Купить молоко | invalid_time"

        # ✅ ПРАВИЛЬНО: Ловить ValueError
        with pytest.raises(ValueError):
            sample_reminder_parser.parse(reminder_text, user_id=123)
