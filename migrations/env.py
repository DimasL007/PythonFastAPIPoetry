import asyncio
import sys
from pathlib import Path

# Робимо шлях абсолютним і ставимо його на ПЕРШЕ місце (індекс 0) в пошуку
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from config import settings
from asyncsession_maker import Base
# Імпортуємо моделі, щоб Alembic їх побачив
from models import User, UserProfile, Category, Product, Order

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.database_url # Беремо URL з нашого конфігу
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    # Отримуємо секцію конфігу
    section = config.get_section(config.config_ini_section, {})
    # ПЕРЕЗАПИСУЄМО URL на той, що в нашому .env
    section["sqlalchemy.url"] = settings.database_url

    connectable = async_engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Запуск міграцій в онлайн режимі"""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()