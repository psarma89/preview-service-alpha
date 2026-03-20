import sys
from pathlib import Path

from sqlalchemy import create_engine, pool

from alembic import context

# Ensure the service root is on sys.path so we can import api.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.database import Base  # noqa: E402
from api.models import User  # noqa: E402, F401 — registers model metadata
from api.settings import get_settings  # noqa: E402

config = context.config
target_metadata = Base.metadata


def get_url() -> str:
    url = config.get_main_option("sqlalchemy.url")
    if url:
        return url
    return get_settings().database_url


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        version_table="alembic_version_alpha",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_alpha",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
