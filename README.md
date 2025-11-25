# 🔔 Telegram Reminder Bot - README

**Простой и мощный бот-напоминалка для Telegram**

## 📋 Содержание

- [О проекте](#о-проекте)
- [Возможности](#возможности)
- [Требования](#требования)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Архитектура](#архитектура)
- [Примеры](#примеры)
- [Разработка](#разработка)
- [Контрибьютинг](#контрибьютинг)

---

## 🎯 О проекте

**Telegram Reminder Bot** - это асинхронный бот для Telegram, который помнит о важных событиях и отправляет вам уведомления в нужное время.

Бот создан с использованием лучших практик:
- ✅ **Command Pattern** - чистая архитектура команд
- ✅ **Repository Pattern** - отделение логики от БД
- ✅ **Dependency Injection** - гибкое управление зависимостями
- ✅ **Async/Await** - асинхронная обработка
- ✅ **APScheduler** - надёжное планирование задач

---

## ⚡ Возможности

### Основной функционал:
- ✅ **Создание напоминаний** с разными форматами времени
- ✅ **Списки напоминаний** - просмотр всех активных напоминаний
- ✅ **Отмена напоминаний** - удалить по ID
- ✅ **Приоритеты** - low, medium, high
- ✅ **Повторения** - once, daily, weekly, monthly
- ✅ **Категории** - организация напоминаний

### Форматы времени:
```
18:00                    → Сегодня в 18:00
завтра 15:30            → Завтра в 15:30
через 2 часа            → Через 2 часа
через 30 минут          → Через 30 минут
2024-11-20 14:00        → Конкретная дата и время
```

### Примеры команд:
```
/remind Купить молоко | 18:00
/remind Встреча | завтра 15:30 | HIGH | once
/remind Работа | 09:00 | MEDIUM | daily
/reminders
/cancel_reminder 5
```

---

## 📦 Требования

- **Python 3.9+**
- **PostgreSQL 12+** (или SQLite для разработки)
- **Telegram Bot Token**

### Зависимости:
```
aiogram==3.1.0
asyncpg==0.27.0
apscheduler==3.10.0
python-dotenv==1.0.0
sqlalchemy==2.0.0
alembic==1.13.0
```

---

## 🚀 Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/telegram-reminder-bot.git
cd telegram-reminder-bot
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Создание базы данных
```bash
# PostgreSQL
createdb reminder_bot_db

# Или используй SQLite (для разработки)
# Будет создана автоматически
```

### 5. Миграции
```bash
alembic upgrade head
```

### 6. Запуск бота
```bash
python main.py
```

---

## 🔧 Конфигурация

### Файл `.env`

Создай файл `.env` в корне проекта:

```env
# Telegram
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=123456789,987654321

# База данных
DATABASE_URL=postgresql+asyncpg://user:password@localhost/reminder_bot_db
# Или для SQLite:
# DATABASE_URL=sqlite+aiosqlite:///./reminder_bot.db

# Окружение
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

### Получение Bot Token

1. Открой [@BotFather](https://t.me/botfather) в Telegram
2. Отправь `/newbot`
3. Следуй инструкциям
4. Скопируй токен в `.env`

---

## 💻 Использование

### Основные команды

#### `/start`
Приветствие и справка по использованию

```
👋 Привет! Я бот-напоминалка.

📝 Основные команды:
/remind - Создать напоминание
/reminders - Показать все напоминания
/cancel_reminder - Отменить напоминание
/help - Справка
```

#### `/remind <текст> | <время> [| приоритет] [| повтор]`
Создать новое напоминание

**Примеры:**
```
/remind Купить молоко | 18:00

/remind Встреча с командой | завтра 15:30

/remind Позвонить маме | через 2 часа

/remind Рабочая встреча | 09:00 | HIGH | daily

/remind Купить подарок | 2024-11-20 19:00 | MEDIUM | once
```

**Поддерживаемые форматы времени:**
- `HH:MM` - Сегодня в указанное время (если прошло → на завтра)
- `завтра HH:MM` - Завтра в указанное время
- `через X часов` - Через X часов
- `через X минут` - Через X минут
- `YYYY-MM-DD HH:MM` - Конкретная дата и время

**Приоритеты:**
- `LOW` - Низкий приоритет
- `MEDIUM` - Средний приоритет (по умолчанию)
- `HIGH` - Высокий приоритет

**Повторения:**
- `ONCE` - Один раз (по умолчанию)
- `DAILY` - Каждый день в указанное время
- `WEEKLY` - Каждую неделю
- `MONTHLY` - Каждый месяц

#### `/reminders`
Показать все ваши напоминания

```
📋 Ваши напоминания:

#1 📝 Купить молоко
⏰ 16.11.2025 18:00
🔔 medium | 🔄 once
━━━━━━━━━━━

#2 📝 Встреча с командой
⏰ 17.11.2025 15:30
🔔 high | 🔄 daily
━━━━━━━━━━━
```

#### `/cancel_reminder <ID>`
Отменить напоминание по ID

```
/cancel_reminder 1
✅ Напоминание отменено
```

#### `/help`
Получить справку

---

## 🏗️ Архитектура

### Структура проекта

```
telegram-reminder-bot/
├── app/
│   ├── entities/
│   │   └── reminder.py              # Модель Reminder
│   ├── repositories/
│   │   ├── base.py                  # Базовый репозиторий
│   │   ├── reminder_repository.py   # Репозиторий напоминаний
│   │   └── postgres_repository.py   # PostgreSQL реализация
│   ├── services/
│   │   └── reminder_service.py      # Бизнес-логика
│   ├── commands/
│   │   ├── base.py                  # Базовая команда
│   │   ├── create_reminder_cmd.py   # Создание напоминания
│   │   ├── list_reminders_cmd.py    # Список напоминаний
│   │   └── cancel_reminder_cmd.py   # Отмена напоминания
│   ├── dispatchers/
│   │   ├── reminder_dispatcher.py     # Обработчики команд
│   ├── schedulers/
│   │   └── reminder_scheduler.py    # APScheduler
│   ├── parsers/
│   │   └── reminder_parser.py       # Парсер входных данных
│   ├── database/
│   │   ├── connection.py            # Подключение к БД
│   │   ├── models.py                # SQLAlchemy модели
│   │   └── migrations/              # Alembic миграции
│   ├── config.py                    # Конфигурация
│   └── di_container.py              # Dependency Injection
├── tests/
│   ├── test_parser.py               # Тесты парсера
│   ├── test_service.py              # Тесты сервиса
│   └── test_repositories.py         # Тесты репозиториев
├── main.py                          # Точка входа
├── requirements.txt                 # Зависимости
├── .env.example                     # Пример .env
├── README.md                        # Этот файл
└── docker-compose.yml               # Docker контейнеры
```

### Слои архитектуры

```
┌─────────────────────────────────────────┐
│     Telegram Bot Handlers               │
│  (/remind, /reminders, /cancel_remind)  │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│        Command Pattern                  │
│ CreateReminderCommand, CancelCmd, etc   │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│      Service Layer (Business Logic)     │
│         ReminderService                 │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│    Repository Pattern (Data Access)     │
│ IReminderRepository, PostgresRepo, etc  │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│     Database (PostgreSQL / SQLite)      │
└─────────────────────────────────────────┘

Также:
- Scheduler: APScheduler для отправки напоминаний
- Parser: ReminderInputParser для парсирования команд
- DI Container: Управление зависимостями
```

---

## 📝 Примеры

### Пример 1: Простое напоминание

```bash
Пользователь пишет:
/remind Купить молоко | 18:00

Ответ бота:
✅ Напоминание создано!

📝 Купить молоко
⏰ 16.11.2025 18:00
🔔 medium
🔄 once

[Через время...]
🔔 НАПОМИНАНИЕ!

📝 Купить молоко
⏰ 16.11.2025 18:00
🔔 MEDIUM
```

### Пример 2: Повторяющееся напоминание

```bash
Пользователь пишет:
/remind Встреча с командой | 09:00 | HIGH | daily

Ответ бота:
✅ Напоминание создано!

📝 Встреча с командой
⏰ 16.11.2025 09:00
🔔 high
🔄 daily

[Каждый день в 09:00 бот отправляет напоминание]
```

### Пример 3: Относительное время

```bash
Пользователь пишет:
/remind Позвонить маме | через 30 минут | HIGH

Ответ бота:
✅ Напоминание создано!

📝 Позвонить маме
⏰ 16.11.2025 18:45 (текущее время + 30 минут)
🔔 high
🔄 once
```

### Пример 4: Список напоминаний

```bash
Пользователь пишет:
/reminders

Ответ бота:
📋 Ваши напоминания:

#1 📝 Купить молоко
⏰ 16.11.2025 18:00
🔔 medium | 🔄 once

#2 📝 Встреча
⏰ 17.11.2025 15:30
🔔 high | 🔄 daily

#3 📝 Позвонить маме
⏰ 16.11.2025 18:45
🔔 high | 🔄 once
```

### Пример 5: Отмена напоминания

```bash
Пользователь пишет:
/cancel_reminder 1

Ответ бота:
✅ Напоминание отменено
```

---

## 🧪 Разработка

### Установка для разработки

```bash
pip install -r requirements-dev.txt
```

### Запуск тестов

```bash
pytest

# С покрытием
pytest --cov=app tests/

# Конкретный тест
pytest tests/test_parser.py::test_parse_time
```

### Запуск в режиме разработки

```bash
# С автоперезагрузкой
python -m uvicorn main:app --reload

# Или просто
python main.py
```

### Логирование

```
DEBUG: Detailig информация
INFO: Основная информация
WARNING: Предупреждения
ERROR: Ошибки
CRITICAL: Критические ошибки
```

Смотри в `logs/reminder_bot.log`

---

## 🤝 Контрибьютинг

Вклады приветствуются!

### Процесс:

1. **Fork** репозиторий
2. **Создай** ветку (`git checkout -b feature/AmazingFeature`)
3. **Коммитай** изменения (`git commit -m 'Add some AmazingFeature'`)
4. **Push** на ветку (`git push origin feature/AmazingFeature`)
5. **Открой** Pull Request

### Требования:

- ✅ Код следует PEP 8
- ✅ Добавлены тесты для новых функций
- ✅ Документация обновлена
- ✅ Commit сообщения понятны и информативны

---

## 📚 Дополнительные ресурсы

- [Aiogram документация](https://docs.aiogram.dev/)
- [APScheduler документация](https://apscheduler.readthedocs.io/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)

---

## 🐛 Найдена ошибка?

Откройте [Issue](https://github.com/yourusername/telegram-reminder-bot/issues) с описанием проблемы.

---

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

---

## 👨‍💻 Автор

- **Ваше имя** - [@yourgithub](https://github.com/yourusername)

---

## 📊 Статистика

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Development-yellow)

---

## ✨ Спасибо!

Спасибо за использование Telegram Reminder Bot!

Если тебе понравился проект, поставь ⭐ звезду!

---

## 🗺️ Roadmap

### v1.0 (Текущая версия)
- [x] Создание напоминаний
- [x] Список напоминаний
- [x] Отмена напоминаний
- [x] Поддержка приоритетов
- [x] Повторяющиеся напоминания

### v1.1 (Планируется)
- [ ] Редактирование напоминаний
- [ ] Снуз функция (напомнить через 5 минут)
- [ ] Категории и теги
- [ ] Поиск напоминаний
- [ ] Экспорт в iCal

### v1.2 (Планируется)
- [ ] Напоминания в групповых чатах
- [ ] Повторяющиеся напоминания по дням недели
- [ ] Уведомления перед событием
- [ ] Интеграция с Google Calendar
- [ ] Web интерфейс

### v2.0 (Долгосрочное видение)
- [ ] Синхронизация между устройствами
- [ ] Совместные напоминания
- [ ] AI-ассистент для парсирования естественного языка
- [ ] Мобильное приложение

---

## 📞 Поддержка

Нужна помощь?

- 📧 Email: support@example.com
- 💬 Telegram: [@yourbot_support](https://t.me/yourbot_support)
- 📖 Документация: [docs.example.com](https://docs.example.com)

---

**Последнее обновление:** 16 ноября 2025

**Версия:** 1.0.0

Спасибо за использование! 🚀
