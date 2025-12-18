from app.entities.reminder import Reminder as ReminderEntity, ReminderStatus as ReminderStatusEntity, RepeatedValue as RepeatedValueEntity, Priority as PriorityEntity
from app.database.models import Reminder as ReminderDb, RepeatedValue as RepeatedValueDb, Status as ReminderStatusDb

def from_model_to_entity(model: ReminderDb) -> ReminderEntity:
    return ReminderEntity(
        id=model.id,
        telegram_id=model.telegram_id,
        text=model.text,
        remind_at=model.remind_at,
        priority=PriorityEntity(model.priority.value.lower()),
        status=ReminderStatusEntity(model.status.value.lower()),
        created_at=model.created_at,
        repeated_value=RepeatedValueEntity(model.repeated_value.value.lower())
    )