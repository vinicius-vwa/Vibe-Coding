import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.models import Base

load_dotenv()


def get_database_url(database_url: Optional[str] = None) -> str:
    """Retorna a URL de conexão apropriada para SQLite ou MySQL."""
    if database_url:
        return database_url

    app_env = os.getenv("APP_ENV", "local").lower()
    mysql_url = os.getenv("MYSQL_DATABASE_URL")

    if app_env == "production" and mysql_url:
        return mysql_url

    return os.getenv("SQLITE_DATABASE_URL", "sqlite:///./local.db")


def get_engine(database_url: Optional[str] = None) -> Engine:
    url = get_database_url(database_url)
    engine_kwargs = {}

    if url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    return create_engine(url, **engine_kwargs)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return SessionLocal()
