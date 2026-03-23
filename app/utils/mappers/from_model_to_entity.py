from app.models import (
    Reminder,
    Status,
    RepeatedValue,
    Priority,
    Platform,
)
from app.entities import ReminderDb


def from_model_to_entity(model: ReminderDb) -> Reminder:
    return Reminder(
        id=model.id,
        user_id=model.user_id,
        text=model.text,
        remind_at=model.remind_at,
        priority=Priority(model.priority.value.lower()),
        status=Status(model.status.value.lower()),
        created_at=model.created_at,
        repeated_value=RepeatedValue(model.repeated_value.value.lower()),
        platform=Platform(model.platform.value.upper()),
    )
