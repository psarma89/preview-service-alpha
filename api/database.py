from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .settings import get_settings


class Base(DeclarativeBase):
    pass


_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            future=True,
        )
    return _engine


def get_session_factory() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return _SessionLocal


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    with session_scope() as db:
        yield db


def reset_engine() -> None:
    """Reset cached engine/session — used in tests to point at a test DB."""
    global _engine, _SessionLocal
    _engine = None
    _SessionLocal = None
