from typing import Annotated
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from models import Todos

from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
async def read_all(db: db_dependency):
    return db.query(Todos).all()


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8003, reload=True)
