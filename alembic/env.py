# coding: utf-8
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"📁 Project root: {project_root}")
print(f"🐍 Python path: {sys.path[0]}")

try:
    from app.database.models import Base, Reminder
    print("✅ Models imported successfully!")
    print(f"   Base.metadata.tables: {list(Base.metadata.tables.keys())}")
except ImportError as e:
    print(f"❌ Failed to import models: {e}")
    raise

config = context.config
target_metadata = Base.metadata

print(f"✅ target_metadata tables: {list(target_metadata.tables.keys())}")


def run_migrations_offline():
    """Offline migrations."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online migrations."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
