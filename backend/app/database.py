import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Swap DATABASE_URL to a Postgres URL in production, e.g.
# postgresql+psycopg2://user:password@host:5432/washcare
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./washcare.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
