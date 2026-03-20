from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.database import Base, get_db
from api.main import create_app
from api.settings import Settings, get_settings

# In-memory SQLite for fast tests
TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        service_name="service-alpha-test",
        environment="test",
        database_url=TEST_DATABASE_URL,
        api_token="test-token",
    )


@pytest.fixture
def client(db_session: Session, test_settings: Settings) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_settings] = lambda: test_settings
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-token"}
