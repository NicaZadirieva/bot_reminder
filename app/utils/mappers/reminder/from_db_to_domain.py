from app.domain import (
    Reminder,
    Status,
    RepeatedValue,
    Priority,
    Platform,
)
from app.entities import ReminderDb


def from_db_to_domain(entity: ReminderDb) -> Reminder:
    return Reminder(
        id=entity.id,
        user_id=entity.user_id,
        text=entity.text,
        remind_at=entity.remind_at,
        priority=Priority(entity.priority.value.lower()),
        status=Status(entity.status.value.lower()),
        created_at=entity.created_at,
        repeated_value=RepeatedValue(entity.repeated_value.value.lower()),
        platform=Platform(entity.platform.value.upper()),
    )
