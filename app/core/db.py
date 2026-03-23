from app.core.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

settings = Settings()  # type: ignore[call-arg]

engine = create_async_engine(
    settings.db.DATABASE_URL,
    echo=False,  # вывод sql-команд отключена
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,  # создание новой сессии после каждого коммита в БД отключена
)
