from app.entities.reminder import Reminder, RepeatedValue, ReminderStatus
from typing import Optional, List, Any
from datetime import datetime, timedelta, timezone as dt_timezone
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
import logging

from app.services.reminder_service import ReminderService
from app.utils.Utils import Utils

logger = logging.getLogger(__name__)


class ReminderScheduler:
    def __init__(self, reminderService: ReminderService, bot: Bot):
        self.reminderService = reminderService
        self.bot = bot
        self.reminders = dict()
        self.tz = timezone('Europe/Moscow')
        self.scheduler = AsyncIOScheduler(timezone=self.tz)

    async def start(self):
        """🚀 Запустить scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("✅ Scheduler запущен")
            await self.load_reminders()

    async def shutdown(self):
        """⏹️ Остановить scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("✅ Scheduler остановлен")

   

    async def load_reminders(self):
        """📥 Загрузить ВСЕ активные напоминания из БД"""
        logger.info("📥 Загружаю напоминания...")
        
        try:
            to_schedule = await self.reminderService.get_all_active_reminders()
            
            for reminder in to_schedule:
                await self.schedule_reminder(reminder)
            
            logger.info(f"✅ Загружено {len(to_schedule)} напоминаний")
        
        except Exception as e:
            logger.error(f"❌ Ошибка при загрузке напоминаний: {e}", exc_info=True)

    async def cancel_reminder_job(self, id: int, user_id: int):
        """❌ Отменить напоминание"""
        try:
            if not self.reminderService.check_if_reminder_exists(id, user_id):
                raise Exception(f"Reminder with id={id} not found")
            
            job_id = f'reminder_{id}'
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"✅ Напоминание #{id} отменено")
            
            if id in self.reminders:
                del self.reminders[id]
                
        except Exception as e:
            logger.error(f"❌ Ошибка при отмене напоминания: {e}", exc_info=True)
            raise

    async def schedule_reminder(self, reminder: Reminder):
        """Запланировать одно напоминание в APScheduler"""
        try:
            # 1️⃣ Создать функцию которая выполнится в нужное время
            async def send_reminder():
                """Эта функция вызовется в reminder.remind_at или по cron"""
                try:
                    if not self.bot:
                        logger.warning(f"⚠️ Bot не инициализирован для напоминания #{reminder.id}")
                        return
                    
                    # Отправить сообщение
                    await self.bot.send_message(
                        chat_id=reminder.telegram_id,
                        text=f"🔔 НАПОМИНАНИЕ!\n\n{reminder.text}"
                    )
                    
                    logger.info(f"✅ Напоминание #{reminder.id} отправлено")
                    
                    # ⚠️ ВАЖНО: менять статус ТОЛЬКО для ONCE
                    # Для DAILY/WEEKLY/MONTHLY оставляем ACTIVE
                    if reminder.repeated_value == RepeatedValue.ONCE:
                        await self.reminderService.cancel_reminder_by_id(reminder.id)
                        # Удалить из активных
                        if reminder.id in self.reminders:
                            del self.reminders[reminder.id]
                
                except Exception as e:
                    logger.error(f"❌ Ошибка при отправке напоминания #{reminder.id}: {e}", exc_info=True)
            
            # 2️⃣ Создать уникальный ID для этой задачи
            job_id = f'reminder_{reminder.id}'

            if reminder.repeated_value == RepeatedValue.ONCE:
                # РАЗОВОЕ НАПОМИНАНИЕ (ONCE)
                # Конвертировать в timezone-aware
                remind_at_aware = Utils._make_aware(reminder.remind_at)
                now = Utils.get_now()
                
                # Только если время ещё не прошло
                if remind_at_aware <= now:
                    logger.warning(f"⏭️ Напоминание #{reminder.id} пропущено (время в прошлом: {remind_at_aware})")
                    return
                
                self.scheduler.add_job(
                    send_reminder,
                    'date',
                    run_date=remind_at_aware,
                    id=job_id,
                    replace_existing=True
                )
                self.reminders[reminder.id] = job_id
                logger.info(
                    f"   ✅ #{reminder.id}: {reminder.text} → {remind_at_aware.strftime('%Y-%m-%d %H:%M')}"
                )

            elif reminder.repeated_value == RepeatedValue.DAILY:
                # ЕЖЕДНЕВНОЕ НАПОМИНАНИЕ (DAILY)
                self.scheduler.add_job(
                    send_reminder,
                    'cron',
                    hour=reminder.remind_at.hour,
                    minute=reminder.remind_at.minute,
                    id=job_id,
                    replace_existing=True
                )
                self.reminders[reminder.id] = job_id
                logger.info(
                    f"   ♻️ ЕЖЕДНЕВНО: #{reminder.id}: {reminder.text} → каждый день в {reminder.remind_at.strftime('%H:%M')}"
                )

            elif reminder.repeated_value == RepeatedValue.WEEKLY:
                # ЕЖЕНЕДЕЛЬНОЕ НАПОМИНАНИЕ (WEEKLY)
                # weekday: 0=Mon, 1=Tue, ..., 6=Sun
                self.scheduler.add_job(
                    send_reminder,
                    'cron',
                    day_of_week=reminder.remind_at.weekday(),
                    hour=reminder.remind_at.hour,
                    minute=reminder.remind_at.minute,
                    id=job_id,
                    replace_existing=True
                )
                self.reminders[reminder.id] = job_id
                logger.info(
                    f"   🔁 ЕЖЕНЕДЕЛЬНО: #{reminder.id}: {reminder.text} → каждый {reminder.remind_at.strftime('%A')} в {reminder.remind_at.strftime('%H:%M')}"
                )

            elif reminder.repeated_value == RepeatedValue.MONTHLY:
                # ЕЖЕМЕСЯЧНОЕ НАПОМИНАНИЕ (MONTHLY)
                # ⚠️ Проблема: если день > 28, то февраль не сработает
                # Решение: использовать 'last_day_of_month' или обработать исключение
                day = reminder.remind_at.day
                
                # Проверка: если день > 28, напомним об этом
                if day > 28:
                    logger.warning(
                        f"⚠️ Напоминание #{reminder.id} на {day}-го числа может не сработать "
                        f"в месяцы с меньшим количеством дней (февраль, апрель и т.д.)"
                    )
                
                self.scheduler.add_job(
                    send_reminder,
                    'cron',
                    day=day,
                    hour=reminder.remind_at.hour,
                    minute=reminder.remind_at.minute,
                    id=job_id,
                    replace_existing=True
                )
                self.reminders[reminder.id] = job_id
                logger.info(
                    f"   🗓️ ЕЖЕМЕСЯЧНО: #{reminder.id}: {reminder.text} → каждый месяц, {day}-го в {reminder.remind_at.strftime('%H:%M')}"
                )
            elif reminder.repeated_value == RepeatedValue.YEARLY:
                 # ЕЖЕГОДНОЕ НАПОМИНАНИЕ (YEARLY)
                month = reminder.remind_at.month
                day = reminder.remind_at.day
            
                # Проверка: если 29 февраля, напомним об этом
                if month == 2 and day == 29:
                    logger.warning(
                        f"⚠️ Напоминание #{reminder.id} на 29 февраля может не сработать "
                        f"в невисокосные годы"
                    )
            
                self.scheduler.add_job(
                    send_reminder,
                    'cron',
                    month=month,
                    day=day,
                    hour=reminder.remind_at.hour,
                    minute=reminder.remind_at.minute,
                    id=job_id,
                    replace_existing=True
                )
                self.reminders[reminder.id] = job_id
                logger.info(
                    f"   📅 ЕЖЕГОДНО: #{reminder.id}: {reminder.text} → каждый год, "
                    f"{reminder.remind_at.strftime('%d %B')} в {reminder.remind_at.strftime('%H:%M')}"
                )

        except Exception as e:
            logger.error(f"❌ Ошибка при планировании напоминания #{reminder.id}: {e}", exc_info=True)
