#!/bin/sh
set -e

# Run migrations if RUN_MIGRATIONS is set (used in ephemeral environments)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running alembic migrations..."
    alembic upgrade head

    echo "Running seed script..."
    python -m scripts.seed || true
fi

exec uvicorn api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
