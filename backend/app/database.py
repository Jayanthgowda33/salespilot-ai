"""
This file sets up the connection to PostgreSQL using SQLAlchemy.
Every other file that needs to talk to the database imports
`get_db` from here (it hands out one DB session per request and
closes it automatically when the request is done).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
