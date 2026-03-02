from app.entities import ReminderEntity, StatusEntity, RepeatedValueEntity, PriorityEntity
from app.database import ReminderDb

def from_model_to_entity(model: ReminderDb) -> ReminderEntity:
    return ReminderEntity(
        id=model.id,
        telegram_id=model.telegram_id,
        text=model.text,
        remind_at=model.remind_at,
        priority=PriorityEntity(model.priority.value.lower()),
        status=StatusEntity(model.status.value.lower()),
        created_at=model.created_at,
        repeated_value=RepeatedValueEntity(model.repeated_value.value.lower())
    )