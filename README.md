# Service Alpha — Users API

FastAPI CRUD microservice for managing users.

## Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for running tests/lint locally)
- [uv](https://docs.astral.sh/uv/) (for local Python dependency management)

## Quick Start

```bash
# Set up local env (copy and customize)
cp .env.local.example .env.local

# First-time setup: build image, run migrations, seed sample data
make setup

# Start the service
make up
```

The API is available at **http://localhost:9001/docs** (Swagger UI).

## Common Commands

```bash
make up              # Start the service
make down            # Stop the service
make reset           # Stop and wipe database volume

make migrate         # Run database migrations
make migrations MESSAGE="add phone number"  # Generate a new migration
make seed            # Seed sample data (idempotent)
make seed-nuke       # Wipe and re-seed

make test            # Run tests (uses in-memory SQLite)
make lint            # Lint with ruff
make fmt             # Auto-format with ruff
make check           # Lint + test

make shell-db        # Open a psql shell against local Postgres
```

Run `make help` for the full list.

## API Endpoints

All endpoints except `/health` require `Authorization: Bearer <token>` (default local token: `dev-token`).

```
GET    /health              — Health check (no auth)
POST   /api/users           — Create a user
GET    /api/users            — List users
GET    /api/users/{id}       — Get a user
PUT    /api/users/{id}       — Update a user
DELETE /api/users/{id}       — Delete a user
```

Examples:

```bash
# Create
curl -X POST http://localhost:9001/api/users \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User", "bio": "Engineer"}'

# List
curl http://localhost:9001/api/users -H "Authorization: Bearer dev-token"

# Get by ID
curl http://localhost:9001/api/users/1 -H "Authorization: Bearer dev-token"

# Update
curl -X PUT http://localhost:9001/api/users/1 \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "bio": "Senior Engineer"}'

# Delete
curl -X DELETE http://localhost:9001/api/users/1 -H "Authorization: Bearer dev-token"
```

## Project Structure

```
├── api/
│   ├── main.py            # FastAPI app factory
│   ├── settings.py        # Config via environment variables
│   ├── database.py        # SQLAlchemy engine and session management
│   ├── core/
│   │   └── auth.py        # Bearer token authentication
│   ├── models/
│   │   └── user.py        # SQLAlchemy model
│   ├── routes/
│   │   └── users.py       # API route handlers
│   └── schemas/
│       └── user.py        # Pydantic request/response schemas
├── alembic/               # Database migrations (tracked in alembic_version_alpha)
├── scripts/
│   └── seed.py            # Sample data seeding
├── tests/                 # Pytest suite (SQLite in-memory)
├── Dockerfile
├── docker-compose.yml     # Local dev: Postgres + app + migrate service
├── Makefile
└── pyproject.toml         # Dependencies, ruff config, pytest config
```

## Environment Variables

| Variable       | Default                                          | Description         |
|----------------|--------------------------------------------------|---------------------|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/appdb` | PostgreSQL connection string |
| `API_TOKEN`    | `dev-token`                                      | Bearer token for auth |
| `ENVIRONMENT`  | `local`                                          | Environment name    |
