import sched
import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.reminder_service import ReminderService
from aiogram import Bot
from app.entities.reminder import Reminder, ReminderStatus, RepeatedValue
from datetime import datetime, timezone

@pytest.fixture
def mock_reminder_service():
    service = AsyncMock(spec=ReminderService)
    # Настройка методов по умолчанию
    service.get_all_active_reminders.return_value = []
    service.check_if_reminder_exists.return_value = True
    service.cancel_reminder_by_id = AsyncMock()
    return service

@pytest.fixture
def mock_bot():
    bot = AsyncMock(spec=Bot)
    bot.send_message = AsyncMock()
    return bot

@pytest.fixture
def reminder_scheduler(mock_reminder_service: AsyncMock, mock_bot: AsyncMock):
    from app.schedulers.reminder_scheduler import ReminderScheduler
    scheduler = ReminderScheduler(mock_reminder_service, mock_bot)
    # Можно замокать scheduler внутри, чтобы не запускать реальные задачи
    scheduler.scheduler = AsyncMock()
    scheduler.scheduler.running = False
    return scheduler

@pytest.fixture
def sample_reminder_once():
    return Reminder(
        id=1,
        telegram_id=123,
        text="Test reminder",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.ONCE,
        status=ReminderStatus.ACTIVE
    )

@pytest.fixture
def sample_reminder_daily():
    return Reminder(
        id=1,
        telegram_id=1234,
        text="Test reminder daily",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.DAILY,
        status=ReminderStatus.ACTIVE
    )

@pytest.fixture
def sample_reminder_yearly():
    return Reminder(
        id=1,
        telegram_id=12345,
        text="Test reminder yearly",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.YEARLY,
        status=ReminderStatus.ACTIVE
    )

@pytest.fixture
def sample_reminder_monthly():
    return Reminder(
        id=1,
        telegram_id=123456,
        text="Test reminder monthly",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.MONTHLY,
        status=ReminderStatus.ACTIVE
    )

@pytest.fixture
def sample_reminder_weekly():
    return Reminder(
        id=1,
        telegram_id=123456,
        text="Test reminder weekly",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.WEEKLY,
        status=ReminderStatus.ACTIVE
    )

def test_init(reminder_scheduler):
    scheduler = reminder_scheduler
    assert scheduler.tz.zone == "Europe/Moscow"

@pytest.mark.asyncio
async def test_start(reminder_scheduler):
    scheduler = reminder_scheduler
    scheduler.scheduler.running = False
    scheduler.load_reminders = AsyncMock(return_value=None)

    await scheduler.start()

    scheduler.scheduler.start.assert_called_once()
    scheduler.load_reminders.assert_awaited_once()

@pytest.mark.asyncio
async def test_start_twice(reminder_scheduler):
    scheduler = reminder_scheduler
    scheduler.scheduler.running = False
    scheduler.load_reminders = AsyncMock(return_value=None)

    await scheduler.start()
    await scheduler.start()

    # проверка запуска 1 раз
    scheduler.scheduler.start.assert_called_once()
    scheduler.load_reminders.assert_awaited_once()