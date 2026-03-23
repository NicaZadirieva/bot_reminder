import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import Bot
from datetime import datetime, timezone
from freezegun import freeze_time
from functools import partial

from app.services import ReminderScheduler
from app.services import ReminderService
from app.models import (
    Reminder,
    Status,
    RepeatedValue,
)


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
        status=Status.ACTIVE,
    )


@pytest.fixture
def sample_reminder_daily():
    return Reminder(
        id=1,
        telegram_id=1234,
        text="Test reminder daily",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.DAILY,
        status=Status.ACTIVE,
    )


@pytest.fixture
def sample_reminder_yearly():
    return Reminder(
        id=1,
        telegram_id=12345,
        text="Test reminder yearly",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.YEARLY,
        status=Status.ACTIVE,
    )


@pytest.fixture
def sample_reminder_monthly():
    return Reminder(
        id=1,
        telegram_id=123456,
        text="Test reminder monthly",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.MONTHLY,
        status=Status.ACTIVE,
    )


@pytest.fixture
def sample_reminder_weekly():
    return Reminder(
        id=1,
        telegram_id=123456,
        text="Test reminder weekly",
        remind_at=datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc),
        repeated_value=RepeatedValue.WEEKLY,
        status=Status.ACTIVE,
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
async def test_stop(reminder_scheduler):
    scheduler = reminder_scheduler
    scheduler.scheduler.running = True
    scheduler.load_reminders = AsyncMock(return_value=None)

    await scheduler.shutdown()

    scheduler.scheduler.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_load_reminders(
    mocker,
    mock_reminder_service,
    reminder_scheduler,
    sample_reminder_once,
    sample_reminder_daily,
    sample_reminder_weekly,
    sample_reminder_monthly,
    sample_reminder_yearly,
):
    scheduler = reminder_scheduler
    service = mock_reminder_service

    # Мокаем schedule_reminder (асинхронный метод)
    mock_schedule = mocker.patch.object(
        scheduler, "schedule_reminder", new_callable=AsyncMock
    )

    # Настраиваем возврат активных напоминаний
    reminders = [
        sample_reminder_once,
        sample_reminder_daily,
        sample_reminder_weekly,
        sample_reminder_monthly,
        sample_reminder_yearly,
    ]
    service.get_all_active_reminders.return_value = reminders

    await scheduler.load_reminders()

    assert mock_schedule.await_count == len(reminders)
    mock_schedule.assert_has_awaits([mocker.call(r) for r in reminders], any_order=True)


@pytest.mark.asyncio
async def test_schedule_reminders(
    mocker,
    reminder_scheduler,
    sample_reminder_once,
    sample_reminder_daily,
    sample_reminder_weekly,
    sample_reminder_monthly,
    sample_reminder_yearly,
):
    scheduler = reminder_scheduler

    # мок всех методов для создания таски
    mock_create_once_task = mocker.patch.object(scheduler, "__create_once_task__")

    mock_create_daily_task = mocker.patch.object(scheduler, "__create_daily_task__")

    mock_create_weekly_task = mocker.patch.object(scheduler, "__create_weekly_task__")

    mock_create_monthly_task = mocker.patch.object(scheduler, "__create_monthly_task__")

    mock_create_yearly_task = mocker.patch.object(scheduler, "__create_yearly_task__")

    # Действия
    await scheduler.schedule_reminder(sample_reminder_once)
    await scheduler.schedule_reminder(sample_reminder_daily)
    await scheduler.schedule_reminder(sample_reminder_weekly)
    await scheduler.schedule_reminder(sample_reminder_monthly)
    await scheduler.schedule_reminder(sample_reminder_yearly)

    # Проверки
    assert mock_create_once_task.call_count == 1
    assert mock_create_daily_task.call_count == 1
    assert mock_create_weekly_task.call_count == 1
    assert mock_create_monthly_task.call_count == 1
    assert mock_create_yearly_task.call_count == 1

    mock_create_once_task.assert_has_calls([mocker.call(sample_reminder_once)])
    mock_create_daily_task.assert_has_calls([mocker.call(sample_reminder_daily)])
    mock_create_weekly_task.assert_has_calls([mocker.call(sample_reminder_weekly)])
    mock_create_monthly_task.assert_has_calls([mocker.call(sample_reminder_monthly)])
    mock_create_yearly_task.assert_has_calls([mocker.call(sample_reminder_yearly)])


@pytest.mark.asyncio
async def test_send_reminder(
    mocker,
    mock_reminder_service,
    reminder_scheduler,
    sample_reminder_once,
    sample_reminder_daily,
    sample_reminder_weekly,
    sample_reminder_monthly,
    sample_reminder_yearly,
):
    scheduler = reminder_scheduler
    service = mock_reminder_service

    # мок вызова отмены напоминания
    mock_cancel_reminder = mocker.patch.object(
        service, "cancel_reminder_by_id", new_callable=AsyncMock
    )
    # Действия
    await scheduler.__send_reminder__(sample_reminder_once)
    # Проверка, вызвана ли отмена
    assert mock_cancel_reminder.await_count == 1

    await scheduler.__send_reminder__(sample_reminder_daily)
    await scheduler.__send_reminder__(sample_reminder_weekly)
    await scheduler.__send_reminder__(sample_reminder_monthly)
    await scheduler.__send_reminder__(sample_reminder_yearly)

    # Проверки
    assert scheduler.bot.send_message.await_count == 5
    # проверка не изменился ли вызов
    assert mock_cancel_reminder.await_count == 1


def test_create_once_task_schedules_job(reminder_scheduler, sample_reminder_once):
    scheduler = reminder_scheduler
    with freeze_time("2025-01-01 10:00:00"):
        # Вызываем метод
        method_name = "__create_once_task__"
        create_once_task = getattr(scheduler, method_name)
        create_once_task(sample_reminder_once)

        # Проверяем вызов add_job
        scheduler.scheduler.add_job.assert_called_once()
        args, kwargs = scheduler.scheduler.add_job.call_args
        func = args[0]
        assert isinstance(func, partial)
        assert func.func == scheduler.__send_reminder__
        assert func.args == (sample_reminder_once,)
        assert kwargs.get("trigger") == "date"
        assert kwargs.get("run_date") == sample_reminder_once.remind_at
        assert kwargs.get("id") == f"reminder_{sample_reminder_once.id}"
        assert kwargs.get("replace_existing") is True

        assert (
            scheduler.reminders.get(sample_reminder_once.id)
            == f"reminder_{sample_reminder_once.id}"
        )


def test_create_daily_task_schedules_job(reminder_scheduler, sample_reminder_daily):
    scheduler = reminder_scheduler
    with freeze_time("2025-01-01 10:00:00"):
        # Вызываем метод
        method_name = "__create_daily_task__"
        create_daily_task = getattr(scheduler, method_name)
        create_daily_task(sample_reminder_daily)

        # Проверяем вызов add_job
        scheduler.scheduler.add_job.assert_called_once()
        args, kwargs = scheduler.scheduler.add_job.call_args
        func = args[0]
        assert isinstance(func, partial)
        assert func.func == scheduler.__send_reminder__
        assert func.args == (sample_reminder_daily,)
        assert kwargs.get("trigger") == "cron"
        assert kwargs.get("hour") == sample_reminder_daily.remind_at.hour
        assert kwargs.get("minute") == sample_reminder_daily.remind_at.minute
        assert kwargs.get("id") == f"reminder_{sample_reminder_daily.id}"
        assert kwargs.get("replace_existing") is True

        assert (
            scheduler.reminders.get(sample_reminder_daily.id)
            == f"reminder_{sample_reminder_daily.id}"
        )


def test_create_weekly_task_schedules_job(reminder_scheduler, sample_reminder_weekly):
    scheduler = reminder_scheduler
    with freeze_time("2025-01-01 10:00:00"):
        # Вызываем метод
        method_name = "__create_weekly_task__"
        create_weekly_task = getattr(scheduler, method_name)
        create_weekly_task(sample_reminder_weekly)

        # Проверяем вызов add_job
        scheduler.scheduler.add_job.assert_called_once()
        args, kwargs = scheduler.scheduler.add_job.call_args
        func = args[0]
        assert isinstance(func, partial)
        assert func.func == scheduler.__send_reminder__
        assert func.args == (sample_reminder_weekly,)
        assert kwargs.get("trigger") == "cron"
        assert kwargs.get("day_of_week") == sample_reminder_weekly.remind_at.weekday()
        assert kwargs.get("hour") == sample_reminder_weekly.remind_at.hour
        assert kwargs.get("minute") == sample_reminder_weekly.remind_at.minute
        assert kwargs.get("id") == f"reminder_{sample_reminder_weekly.id}"
        assert kwargs.get("replace_existing") is True

        assert (
            scheduler.reminders.get(sample_reminder_weekly.id)
            == f"reminder_{sample_reminder_weekly.id}"
        )


def test_create_monthly_task_schedules_job(reminder_scheduler, sample_reminder_monthly):
    scheduler = reminder_scheduler
    with freeze_time("2025-01-01 10:00:00"):
        # Вызываем метод
        method_name = "__create_monthly_task__"
        create_monthly_task = getattr(scheduler, method_name)
        create_monthly_task(sample_reminder_monthly)

        # Проверяем вызов add_job
        scheduler.scheduler.add_job.assert_called_once()
        args, kwargs = scheduler.scheduler.add_job.call_args
        func = args[0]
        assert isinstance(func, partial)
        assert func.func == scheduler.__send_reminder__
        assert func.args == (sample_reminder_monthly,)
        assert kwargs.get("trigger") == "cron"
        assert kwargs.get("day") == sample_reminder_monthly.remind_at.day
        assert kwargs.get("hour") == sample_reminder_monthly.remind_at.hour
        assert kwargs.get("minute") == sample_reminder_monthly.remind_at.minute
        assert kwargs.get("id") == f"reminder_{sample_reminder_monthly.id}"
        assert kwargs.get("replace_existing") is True

        assert (
            scheduler.reminders.get(sample_reminder_monthly.id)
            == f"reminder_{sample_reminder_monthly.id}"
        )


def test_create_yearly_task_schedules_job(reminder_scheduler, sample_reminder_yearly):
    scheduler = reminder_scheduler
    with freeze_time("2025-01-01 10:00:00"):
        # Вызываем метод
        method_name = "__create_yearly_task__"
        create_yearly_task = getattr(scheduler, method_name)
        create_yearly_task(sample_reminder_yearly)

        # Проверяем вызов add_job
        scheduler.scheduler.add_job.assert_called_once()
        args, kwargs = scheduler.scheduler.add_job.call_args
        func = args[0]
        assert isinstance(func, partial)
        assert func.func == scheduler.__send_reminder__
        assert func.args == (sample_reminder_yearly,)
        assert kwargs.get("trigger") == "cron"
        assert kwargs.get("day") == sample_reminder_yearly.remind_at.day
        assert kwargs.get("hour") == sample_reminder_yearly.remind_at.hour
        assert kwargs.get("minute") == sample_reminder_yearly.remind_at.minute
        assert kwargs.get("month") == sample_reminder_yearly.remind_at.month
        assert kwargs.get("id") == f"reminder_{sample_reminder_yearly.id}"
        assert kwargs.get("replace_existing") is True

        assert (
            scheduler.reminders.get(sample_reminder_yearly.id)
            == f"reminder_{sample_reminder_yearly.id}"
        )


@pytest.mark.asyncio
async def test_cancel_reminder_job_success(reminder_scheduler, sample_reminder_once):
    scheduler = reminder_scheduler
    reminder_id = sample_reminder_once.id
    user_id = sample_reminder_once.telegram_id
    job_id = f"reminder_{reminder_id}"

    # Настраиваем сервис: напоминание существует
    scheduler.reminderService.check_if_reminder_exists = AsyncMock(return_value=True)

    # Добавляем запись в self.reminders
    scheduler.reminders[reminder_id] = job_id

    # Настраиваем мок планировщика: get_job возвращает что-то, чтобы remove_job вызвался
    scheduler.scheduler.get_job = MagicMock(return_value=True)
    scheduler.scheduler.remove_job = MagicMock()

    # Действия
    await scheduler.cancel_reminder_job(reminder_id, user_id)

    # Проверяем вызов remove_job с правильным job_id
    scheduler.scheduler.remove_job.assert_called_once_with(job_id)

    # Проверяем, что запись удалена из self.reminders
    assert reminder_id not in scheduler.reminders


@pytest.mark.asyncio
async def test_cancel_reminder_job_no_job_in_scheduler(
    reminder_scheduler, sample_reminder_once
):
    scheduler = reminder_scheduler
    reminder_id = sample_reminder_once.id
    user_id = sample_reminder_once.telegram_id
    job_id = f"reminder_{reminder_id}"

    scheduler.reminderService.check_if_reminder_exists = AsyncMock(return_value=True)

    scheduler.reminders[reminder_id] = job_id
    scheduler.scheduler.get_job = MagicMock(return_value=None)  # задания нет
    scheduler.scheduler.remove_job = MagicMock()

    # Действия
    await scheduler.cancel_reminder_job(reminder_id, user_id)

    # remove_job не должен вызываться, если get_job вернул None
    scheduler.scheduler.remove_job.assert_not_called()


@pytest.mark.asyncio
async def test_cancel_reminder_job_reminder_not_found(
    reminder_scheduler, sample_reminder_once
):
    scheduler = reminder_scheduler
    reminder_id = sample_reminder_once.id
    user_id = sample_reminder_once.telegram_id
    job_id = f"reminder_{reminder_id}"

    # Сервис говорит, что напоминания нет
    scheduler.reminderService.check_if_reminder_exists = AsyncMock(return_value=False)

    # Имитируем, что задание есть в reminders и планировщике (но оно не должно трогаться)
    scheduler.reminders[reminder_id] = job_id
    scheduler.scheduler.get_job = MagicMock(return_value=True)
    scheduler.scheduler.remove_job = MagicMock()

    with pytest.raises(Exception, match=f"Reminder with id={reminder_id} not found"):
        await scheduler.cancel_reminder_job(reminder_id, user_id)

    # Проверяем, что remove_job не вызывался
    scheduler.scheduler.remove_job.assert_not_called()
