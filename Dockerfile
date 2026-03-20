FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml .
RUN uv pip install --system --no-cache .

COPY alembic.ini .
COPY alembic/ ./alembic/
COPY api/ ./api/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY entrypoint.sh .

# Build-time metadata baked into the image
ARG GIT_BRANCH=unknown
ARG GIT_SHA=unknown
ARG IMAGE_TAG=local
ENV GIT_BRANCH=$GIT_BRANCH
ENV GIT_SHA=$GIT_SHA
ENV IMAGE_TAG=$IMAGE_TAG

EXPOSE 8000

# Default: just start uvicorn. Set RUN_MIGRATIONS=true for ephemeral environments
# to run alembic + seed on startup.
CMD ["./entrypoint.sh"]
