import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger("resumeiq.database")

# Normalize URL for SQLAlchemy if needed
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
elif "psycopg" in db_url:
    connect_args["connect_timeout"] = 3

engine = None
try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=True
    )
    # Quick probe
    with engine.connect() as conn:
        pass
    logger.info("Connected to configured database successfully.")
except Exception as e:
    logger.warning(f"Could not connect to configured DATABASE_URL ({e}). Falling back to local SQLite.")
    sqlite_url = "sqlite:///./resumeiq.db"
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides an active database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables in the database."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    Base.metadata.create_all(bind=engine)
