import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------------------------------
# ✅ STEP 1: Add project root to sys.path
# -------------------------------------------------------
# This lets Alembic import backend.* modules properly
# __file__ → backend/alembic/env.py
# ../.. → go up to TASK1 (project root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# -------------------------------------------------------
# ✅ STEP 2: Import Base and all models
# -------------------------------------------------------
from backend.database.database import Base  # SQLAlchemy Base
from backend.model import User, Laptop      # import all models

# -------------------------------------------------------
# ✅ STEP 3: Alembic Config Setup
# -------------------------------------------------------
config = context.config

# Set up Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic where to find your metadata
target_metadata = Base.metadata

# -------------------------------------------------------
# ✅ STEP 4: Migration functions
# -------------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------------
# ✅ STEP 5: Choose online or offline mode
# -------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
