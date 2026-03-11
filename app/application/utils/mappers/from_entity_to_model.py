from app.application.domain.entities import ReminderEntity
from app.infrastructure.database import (
    ReminderDb,
    RepeatedValueDb,
    StatusDb,
    PriorityDb,
)


def from_entity_to_model(entity: ReminderEntity) -> ReminderDb:
    return ReminderDb(
        id=entity.id,
        telegram_id=entity.telegram_id,
        text=entity.text,
        remind_at=entity.remind_at,
        priority=PriorityDb(entity.priority.value.lower()),
        status=StatusDb(entity.status.value.lower()),
        created_at=entity.created_at,
        repeated_value=RepeatedValueDb(entity.repeated_value.value.upper()),
    )
