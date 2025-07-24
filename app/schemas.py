# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

# Sponsor Schemas

class SponsorBase(BaseModel):
    name: str

class SponsorCreate(SponsorBase):
    pass

class Sponsor(SponsorBase):
    id: int

    class Config:
        from_attributes = True

# Task Schemas


class TaskBase(BaseModel):
    task_name: str
    due_date: Optional[str]
    status: Optional[str]
    source: str

class TaskCreate(TaskBase):
    sponsor_id: int

class Task(TaskBase):
    id: int
    sponsor_id: int
    synced_at: datetime
    #ORM- like attributes instead of plain dict
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
# Request Schema for /sync-tasks

class Token(BaseModel):
    access_token: str
    token_type: str

# Token Payload Schema

class TokenData(BaseModel):
    username: Optional[str] = None
class SyncTasksRequest(BaseModel):
    sponsor_id: str  # plain string for matching the POST /sync-tasks contract
    status:Optional[str]=None
class TaskListResponse(BaseModel):
    tasks: List[Task]