from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, schemas, auth
from ..database import get_db
from ..exceptions import raise_not_found_exception, raise_forbidden_exception

router = APIRouter(
    prefix="/sync-tasks",
    tags=["sponsorship-tasks"],
)

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[models.User, Depends(auth.get_current_user)]

@router.post("/", response_model=schemas.TaskListResponse)
def sync_tasks(
    request: schemas.SyncTasksRequest,
    db: db_dependency,
    current_user: current_user_dependency
):
    """
    Synchronizes and returns all tasks for the given sponsor if the current user is authorized.
    Optional filtering by task status can be applied via the request body.

    - Validates the sponsor exists.
    - Checks user-sponsor access control.
    - Returns all associated tasks.
    """

    # Step 1: Find the sponsor
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.name == request.sponsor_id).first()
    if not sponsor:
        raise_not_found_exception("Sponsor not found")

    # Step 2: Check if user has access to this sponsor
    if sponsor not in current_user.sponsors:
        raise_forbidden_exception("You do not have access to this sponsor")

    # Step 3: Fetch all tasks for this sponsor
    query = db.query(models.Task).filter(models.Task.sponsor_id == sponsor.id)

    if request.status:
        query = query.filter(models.Task.status == request.status)
    tasks = query.all()    
    return {"tasks": tasks}
