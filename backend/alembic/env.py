"""Alembic migration environment.

Pulls the database URL from the app's settings (which read .env) and targets the
SQLAlchemy models' metadata, so `alembic revision --autogenerate` and
`alembic upgrade head` work against whatever DATABASE_URL points at.
"""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

# Import the app package so models register on Base.metadata.
from app.config import settings
from app.database import Base
from app import models  # noqa: F401  (import side effect: registers tables)

config = context.config

# NB: we do NOT push the URL into Alembic's config (config.set_main_option),
# because Alembic parses the .ini with ConfigParser, which treats '%' as
# interpolation — and a URL-encoded password (e.g. %3F) would break it. We read
# settings.database_url directly instead.

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(settings.database_url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
