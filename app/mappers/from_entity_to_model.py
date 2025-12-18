from app.entities.reminder import Reminder as ReminderEntity, ReminderStatus as ReminderStatusEntity, RepeatedValue as RepeatedValueEntity, Priority as PriorityEntity
from app.database.models import Reminder as ReminderDb, RepeatedValue as RepeatedValueDb, Status as ReminderStatusDb, Priority as PriorityDb

def from_entity_to_model(entity: ReminderEntity) -> ReminderDb:
    return ReminderDb(
        id=entity.id,
        telegram_id=entity.telegram_id,
        text=entity.text,
        remind_at=entity.remind_at,
        priority=PriorityDb(entity.priority.value.lower()),
        status=ReminderStatusDb(entity.status.value.lower()),
        created_at=entity.created_at,
        repeated_value=RepeatedValueDb(entity.repeated_value.value.upper())
    )