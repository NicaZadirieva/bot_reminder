# APScheduler
from app.database.models import Reminder, RepeatedValue
from app.entities.reminder import ReminderStatus
from repositories.reminder_repository import ReminderRepository
from typing import Optional, List, Any
from datetime import datetime, timedelta
from aiogram import Bot

# TODO: перенести логику в сервис для репо
class ReminderScheduler:
    def __init__(self, session: Any, reminderRepo: ReminderRepository, bot: Bot):
        self.reminderRepo = reminderRepo;
        self.session = session;
        self.bot = bot;
        self.reminders = dict()

    async def load_reminders(self):
        """📥 Загрузить ВСЕ активные напоминания из БД"""
    
        print("📥 Загружаю напоминания...")
    
        try:
            # 1️⃣ Получить ВСЕ напоминания
            all_reminders = await self.reminderRepo.get_all(self.session)
        
            # 2️⃣ Отфильтровать АКТИВНЫЕ
            active = [r for r in all_reminders if r.status == "active"]
        
            # 3️⃣ Отфильтровать БУДУЩИЕ (не прошедшие)
            now = datetime.now()
            future = [r for r in active if r.remind_at > now]
        
            # 4️⃣ Запланировать каждое
            for reminder in future:
                await self.schedule_reminder(reminder)
        
            print(f"✅ Загружено {len(future)} напоминаний")
    
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    async def schedule_reminder(self, reminder: Reminder):
        """Запланировать одно напоминание в APScheduler"""
    
        # 1️⃣ Создать функцию которая выполнится в нужное время
        async def send_reminder():
            """Эта функция вызовется в reminder.remind_at"""
            try:
                # Отправить сообщение
                if self.bot:
                    await self.bot.send_message(
                        chat_id=reminder.telegram_id,
                        text=f"🔔 НАПОМИНАНИЕ!\n\n{reminder.text}"
                    )
            
                    # Обновить статус в БД
                    await self.reminderRepo.update(
                        self.session,
                        reminder.id,
                        status=ReminderStatus.COMPLETED
                    )
            
                    # Удалить из активных
                    if reminder.id in self.reminders:
                        del self.reminders[reminder.id]
            
                    print(f"✅ Напоминание #{reminder.id} отправлено")
                else:
                    print(f"✅ Напоминание #{reminder.id} не может быть отправлено")
        
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
        # 2️⃣ Создать уникальный ID для этой задачи
        job_id = f'reminder_{reminder.id}'

        if reminder.repeated_value == RepeatedValue.ONCE:
            # 3️⃣ Добавить в APScheduler
            self.scheduler.add_job(
                send_reminder,                 # Функция которая выполнится
                'date',                        # Тип триггера (один раз)
                run_date=reminder.remind_at,   # Когда выполнить
                id=job_id,                     # Уникальный ID
                replace_existing=True          # Если уже есть - заменить
            )
    
            # 4️⃣ Запомнить в словаре
            self.reminders[reminder.id] = job_id
    
            # 5️⃣ Логирование
            print(f"   ✅ #{reminder.id}: {reminder.text} → {reminder.remind_at}")

        elif reminder.repeated_value == RepeatedValue.DAILY:
           # → APScheduler cron trigger: каждый день в remind_at.time()
           self.scheduler.add_job(
               send_reminder,
               'cron',
               hour=reminder.remind_at.hour,
               minute=reminder.remind_at.minute,
               id=job_id,
               replace_existing=True
           )
           self.reminders[reminder.id] = job_id
           print(
               f"   ♻️ ЕЖЕДНЕВНО: #{reminder.id}: {reminder.text} → каждый день в {reminder.remind_at.strftime('%H:%M')}"
           )

       # ЕЖЕНЕДЕЛЬНОЕ НАПОМИНАНИЕ (WEEKLY)
        elif reminder.repeated_value == RepeatedValue.WEEKLY:
           # → APScheduler cron trigger: каждую неделю, в день недели и время как у remind_at
           self.scheduler.add_job(
               send_reminder,
               'cron',
               day_of_week=reminder.remind_at.weekday(),  # 0=Mon, 6=Sun
               hour=reminder.remind_at.hour,
               minute=reminder.remind_at.minute,
               id=job_id,
               replace_existing=True
           )
           self.reminders[reminder.id] = job_id
           print(
               f"   🔁 ЕЖЕНЕДЕЛЬНО: #{reminder.id}: {reminder.text} → каждую неделю (день={reminder.remind_at.strftime('%A')}, время={reminder.remind_at.strftime('%H:%M')})"
           )

       # ЕЖЕМЕСЯЧНОЕ НАПОМИНАНИЕ (MONTHLY)
        elif reminder.repeated_value == RepeatedValue.MONTHLY:
           # → APScheduler cron: каждый месяц, такого же числа, в remind_at.time()
           self.scheduler.add_job(
               send_reminder,
               'cron',
               day=reminder.remind_at.day,
               hour=reminder.remind_at.hour,
               minute=reminder.remind_at.minute,
               id=job_id,
               replace_existing=True
           )
           self.reminders[reminder.id] = job_id
           print(
               f"   🗓️ ЕЖЕМЕСЯЧНО: #{reminder.id}: {reminder.text} → каждый месяц, {reminder.remind_at.day}-го в {reminder.remind_at.strftime('%H:%M')}"
           )


