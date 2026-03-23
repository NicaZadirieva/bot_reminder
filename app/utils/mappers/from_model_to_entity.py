from app.entities.entities import (
    ReminderEntity,
    StatusEntity,
    RepeatedValueEntity,
    PriorityEntity,
    PlatformEntity,
)
from app.models.models import Reminder as ReminderDb


def from_model_to_entity(model: ReminderDb) -> ReminderEntity:
    return ReminderEntity(
        id=model.id,
        user_id=model.user_id,
        text=model.text,
        remind_at=model.remind_at,
        priority=PriorityEntity(model.priority.value.lower()),
        status=StatusEntity(model.status.value.lower()),
        created_at=model.created_at,
        repeated_value=RepeatedValueEntity(model.repeated_value.value.lower()),
        platform=PlatformEntity(model.platform.value.upper()),
    )
