# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

#User-Sponsorship association
user_sponsor = Table(
    "user_sponsor",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("sponsor_id", Integer, ForeignKey("sponsors.id"), primary_key=True),
)

class Sponsor(Base):
    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="sponsor")
    users = relationship("User", secondary=user_sponsor, back_populates="sponsors")
    integrations = relationship("Integration", back_populates="sponsor")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    sponsor_id = Column(Integer, ForeignKey("sponsors.id"))
    source = Column(String, nullable=False)            # Salesforce, Asana, etc.
    task_name = Column(String, nullable=False)
    due_date = Column(String)                          # Keep as ISO string for simplicity
    status = Column(String, default="Pending")
    synced_at = Column(DateTime, default=datetime.now(timezone.utc))

    sponsor = relationship("Sponsor", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    sponsors = relationship("Sponsor", secondary=user_sponsor, back_populates="users")


class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True, index=True)
    sponsor_id = Column(Integer, ForeignKey("sponsors.id"))
    system = Column(String)
    api_key = Column(String)
    last_synced_at = Column(DateTime, nullable=True)

    sponsor = relationship("Sponsor", back_populates="integrations")