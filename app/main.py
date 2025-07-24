from fastapi import FastAPI

from .routes import syncTasks

from .database import engine
from .models import Base
from .routes import users, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(syncTasks.router)
