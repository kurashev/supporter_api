import alembic_postgresql_enum
import asyncio
from logging.config import fileConfig

from alembic import context
from environs import Env
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine


from src.infra.database.models import * # noqa

from src.common.config.db import DbConfig
from src.infra.database.models.base import BaseModel

env = Env()
env.read_env()

db = DbConfig.compose(env)

POSTGRES_URI = db.sqlalchemy_uri.render_as_string(hide_password=False)

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = BaseModel.metadata
config.set_main_option('sqlalchemy.url', POSTGRES_URI)


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
