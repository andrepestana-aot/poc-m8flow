from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from m8flow.db.models import Base
import os

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return os.environ["M8FLOW_DATABASE_URI"]

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_m8flow",  # <-- important
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
