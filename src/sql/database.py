from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf.base import SQLITE_DB, SQLITE_DIR

PATH_TO_SQLITE_DB = ""
SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(SQLITE_DIR, SQLITE_DB)}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
