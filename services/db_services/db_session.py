from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Base class for all ORM models
Base = declarative_base()

# check if DB url is set or not
if not DATABASE_URL:
    print("DB URL is not set, please check .env")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set True if you want to see SQL queries in terminal
    future=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    # Create and return a new database session.
    return SessionLocal()
