from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL="sqlite:///./sponsorship_task.db"
#establish a connection to the database
engine= create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal= sessionmaker(autocommit= False, autoflush=False, bind=engine)

#declarative_base: Creates a base class for defining ORM models.
Base= declarative_base()

def get_db():
    """
    Yields a new database session.
    Ensures that the session is closed after the request is done.
    Used in FastAPI route dependencies.
    """
    db= SessionLocal()

    try:
        yield db
    finally:
        db.close()