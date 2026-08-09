from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status

import pytest
from ..models import Todos, Users



SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:123456@127.0.0.1:3306/TestTodoapplicationdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False,poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        'username': 'string',
        'id': 1,
        'user_role': 'admin',
    }

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    # 创建用户
    user = Users(
        id=1,
        email='test@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        hashed_password='hashed_password',
        is_active=True,
        role='admin'
    )

    todo = Todos(
        title = 'learn to code',
        description ='learn to code',
        priority = 5,
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield db, todo

    with engine.connect() as conn:
        conn.execute(text('DELETE FROM TODOS'))
        conn.execute(text('DELETE FROM USERS'))
        conn.commit()


def test_read_all_authenticated(test_todo):
    _, todo = test_todo
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'complete' : False,
        'description' :'learn to code',
        'priority' : 5,
        'title' : 'learn to code',
        'id': todo.id,
        'owner_id' : 1
    }]

def test_read_one_authenticated(test_todo):
    _, todo = test_todo
    response = client.get(f'/todo/{todo.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'complete' : False,
        'description' :'learn to code',
        'priority' : 5,
        'title' : 'learn to code',
        'id': todo.id,
        'owner_id' : 1
    }

def test_read_one_authenticated_not_found():
    response = client.get('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' :'Todo Not Found'
    }


def test_create_todo(test_todo):
    request_data = {
        'title':'new todo',
        'description': 'new todo description',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todo', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()

    model = db.query(Todos).order_by(Todos.id.desc()).first()

    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    _, todo = test_todo
    request_data = {
        'title':'change the title of the todo already saved',
        'description': 'need to learn everyday',
        'priority': 5,
        'complete': False
    }

    response = client.put(f'/todo/{todo.id}', json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()

    model = db.query(Todos).order_by(Todos.id.desc()).first()

    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found():
    request_data = {
        'title':'change the title of the todo already saved',
        'description': 'need to learn everyday',
        'priority': 5,
        'complete': False
    }

    response = client.put('/todo/999', json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}

def test_delete_todo(test_todo):
    _, todo = test_todo
    response = client.delete(f'/todo/{todo.id}')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).order_by(Todos.id.desc()).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/999')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found.'
    }

