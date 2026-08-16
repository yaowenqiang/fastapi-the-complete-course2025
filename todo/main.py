import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Path ,Request, status
from fastapi.responses import RedirectResponse
from .models import Base

from .database import engine
from .routers import auth, todos, admin,user

from fastapi.staticfiles import StaticFiles






app = FastAPI()

app.mount('/static', StaticFiles(directory='todo/static'), name='static')

Base.metadata.create_all(bind=engine)

@app.get('/')
def test(request: Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)

@app.get('/healthy')
def health_check():
    return {'status':'healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)



if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8003, reload=True)
