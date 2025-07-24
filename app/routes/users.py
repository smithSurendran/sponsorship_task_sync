from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, schemas, auth
from ..database import get_db
from ..exceptions import (
    raise_not_found_exception,
    raise_bad_request_exception,
    raise_conflict_exception,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

db_dependency = Annotated[Session, Depends(get_db)]

# User Registration Endpoint
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise_conflict_exception("Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
