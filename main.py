from app.entities.reminder import Reminder, Priority
from datetime import datetime, timedelta

reminder = Reminder(
    telegram_id=123456789,
    text="Купить молоко",
    remind_at=datetime.now() + timedelta(hours=2),
    priority=Priority.HIGH
)

print(reminder)
# Reminder(telegram_id=123456789, text='Купить молоко', ...)

print(f"Активное: {reminder.is_active()}")  # True

reminder.mark_completed()
print(f"Статус: {reminder.status}")  # ReminderStatus.COMPLETED