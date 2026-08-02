from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

import models
from models import Todos

from database import engine, SessionLocal
from routers import auth, todos, admin,user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)



if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8003, reload=True)
